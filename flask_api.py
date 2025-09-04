#!/usr/bin/env python3
"""
Flask API for Image Quality Analysis
Backend service for Flutter mobile apps
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from PIL import Image
import time
import os
from optimized_quality_check import optimized_quality_check

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

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
        'version': '1.0.0'
    })

@app.route('/analyze-single', methods=['POST'])
def analyze_single_image():
    """Analyze single image quality"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Convert base64 to image
        image = base64_to_image(data['image'])
        
        # Analyze image quality
        start_time = time.time()
        score, category, process_time = optimized_quality_check(image)
        total_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'quality_score': float(score),
            'category': category,
            'processing_time': float(process_time),
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
            return jsonify({'error': 'No images data provided'}), 400
        
        images_data = data['images']
        if not isinstance(images_data, list):
            return jsonify({'error': 'Images must be a list'}), 400
        
        if len(images_data) == 0:
            return jsonify({'error': 'No images provided'}), 400
        
        if len(images_data) > 50:  # Limit batch size
            return jsonify({'error': 'Maximum 50 images per batch'}), 400
        
        results = []
        total_start_time = time.time()
        
        for i, image_data in enumerate(images_data):
            try:
                # Convert base64 to image
                image = base64_to_image(image_data)
                
                # Analyze image quality
                score, category, process_time = optimized_quality_check(image)
                
                results.append({
                    'index': i,
                    'quality_score': float(score),
                    'category': category,
                    'processing_time': float(process_time),
                    'success': True
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'success': False
                })
        
        total_time = time.time() - total_start_time
        
        # Calculate summary statistics
        successful_results = [r for r in results if r['success']]
        if successful_results:
            scores = [r['quality_score'] for r in successful_results]
            categories = [r['category'] for r in successful_results]
            
            summary = {
                'total_images': len(images_data),
                'successful_analyses': len(successful_results),
                'failed_analyses': len(results) - len(successful_results),
                'average_score': float(np.mean(scores)),
                'best_score': float(min(scores)),
                'worst_score': float(max(scores)),
                'category_distribution': {
                    'Good': categories.count('Good'),
                    'Moderate': categories.count('Moderate'),
                    'Bad': categories.count('Bad')
                },
                'total_processing_time': float(total_time)
            }
        else:
            summary = {
                'total_images': len(images_data),
                'successful_analyses': 0,
                'failed_analyses': len(results),
                'error': 'All analyses failed'
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

@app.route('/analyze-file', methods=['POST'])
def analyze_uploaded_file():
    """Analyze uploaded image file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read image from uploaded file
        image_data = file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Analyze image quality
        start_time = time.time()
        score, category, process_time = optimized_quality_check(image)
        total_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'quality_score': float(score),
            'category': category,
            'processing_time': float(process_time),
            'total_time': float(total_time),
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

if __name__ == '__main__':
    print("🚀 Starting Image Quality Analysis API...")
    print("📱 Ready for Flutter mobile app integration")
    print("🌐 API Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /analyze-single - Analyze single image")
    print("   POST /analyze-batch - Analyze multiple images")
    print("   POST /analyze-file - Analyze uploaded file")
    print()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
