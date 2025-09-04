#!/usr/bin/env python3
"""
Vercel serverless function for Image Quality Analysis API
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from PIL import Image
import time

# Simple quality check function for Vercel
def optimized_quality_check(img_input, resize_dim=(300, 300)):
    """Simple image quality check optimized for Vercel"""
    if img_input is None:
        return 100.0, "Bad", 0.0
    
    try:
        # Resize image for faster processing
        img_resized = cv2.resize(img_input, resize_dim, interpolation=cv2.INTER_AREA)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance (sharpness)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate noise level
        noise = np.std(gray)
        
        # Calculate contrast
        contrast = np.std(gray)
        
        # Simple quality scoring
        if laplacian_var > 200 and noise < 30:
            return 15.0, "Good", 0.001
        elif laplacian_var > 100 and noise < 50:
            return 35.0, "Moderate", 0.001
        else:
            return 55.0, "Bad", 0.001
            
    except Exception as e:
        return 100.0, "Error", 0.0

app = Flask(__name__)
CORS(app)

def base64_to_image(base64_string):
    """Convert base64 string to OpenCV image"""
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Convert to OpenCV format (BGR)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
    except Exception as e:
        raise ValueError(f"Invalid image data: {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Image Quality Analysis API',
        'version': '1.0.0',
        'platform': 'Vercel'
    })

@app.route('/analyze-single', methods=['POST'])
def analyze_single_image():
    """Analyze single image quality"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        # Convert base64 to image
        image = base64_to_image(data['image'])
        
        # Analyze image quality
        start_time = time.time()
        score, category, processing_time = optimized_quality_check(image)
        total_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'quality_score': float(score),
            'category': category,
            'processing_time': float(processing_time),
            'total_time': float(total_time),
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyze-batch', methods=['POST'])
def analyze_batch_images():
    """Analyze multiple images in batch"""
    try:
        data = request.get_json()
        
        if not data or 'images' not in data:
            return jsonify({
                'success': False,
                'error': 'No images data provided'
            }), 400
        
        images_data = data['images']
        if not isinstance(images_data, list) or len(images_data) == 0:
            return jsonify({
                'success': False,
                'error': 'Images must be a non-empty array'
            }), 400
        
        # Limit batch size for Vercel
        if len(images_data) > 10:
            return jsonify({
                'success': False,
                'error': 'Maximum 10 images allowed per batch'
            }), 400
        
        results = []
        total_processing_time = 0
        successful_analyses = 0
        failed_analyses = 0
        scores = []
        
        for i, image_data in enumerate(images_data):
            try:
                # Convert base64 to image
                image = base64_to_image(image_data)
                
                # Analyze image quality
                start_time = time.time()
                score, category, processing_time = optimized_quality_check(image)
                total_time = time.time() - start_time
                
                results.append({
                    'index': i,
                    'quality_score': float(score),
                    'category': category,
                    'processing_time': float(processing_time),
                    'success': True
                })
                
                scores.append(float(score))
                total_processing_time += processing_time
                successful_analyses += 1
                
            except Exception as e:
                results.append({
                    'index': i,
                    'quality_score': 0,
                    'category': 'Error',
                    'processing_time': 0,
                    'success': False,
                    'error': str(e)
                })
                failed_analyses += 1
        
        # Calculate summary
        category_distribution = {'Good': 0, 'Moderate': 0, 'Bad': 0}
        for result in results:
            if result['success']:
                category_distribution[result['category']] += 1
        
        summary = {
            'total_images': len(images_data),
            'successful_analyses': successful_analyses,
            'failed_analyses': failed_analyses,
            'average_score': float(np.mean(scores)) if scores else 0,
            'best_score': float(np.min(scores)) if scores else 0,
            'worst_score': float(np.max(scores)) if scores else 0,
            'category_distribution': category_distribution,
            'total_processing_time': float(total_processing_time)
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': summary,
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
