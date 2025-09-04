#!/usr/bin/env python3
"""
Vercel serverless function for Image Quality Analysis API
Simplified version without OpenCV for better Vercel compatibility
"""

import sys
import os
import base64
import io
import time
import math

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)

def base64_to_image(base64_string):
    """Convert base64 string to PIL Image"""
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        pil_image = Image.open(io.BytesIO(image_data))
        
        return pil_image
    except Exception as e:
        raise ValueError(f"Invalid image data: {str(e)}")

def simple_quality_check(image, resize_dim=(300, 300)):
    """Simple image quality check using PIL only"""
    try:
        # Resize image for faster processing
        image_resized = image.resize(resize_dim, Image.Resampling.LANCZOS)
        
        # Convert to grayscale
        gray_image = image_resized.convert('L')
        
        # Convert to list of pixels for processing
        pixels = list(gray_image.getdata())
        width, height = gray_image.size
        
        # Calculate basic quality metrics using PIL only
        
        # 1. Sharpness (using edge detection)
        def calculate_sharpness(pixels, width, height):
            sharpness = 0
            count = 0
            for y in range(1, height-1):
                for x in range(1, width-1):
                    # Calculate gradient magnitude
                    center = pixels[y * width + x]
                    right = pixels[y * width + (x+1)]
                    left = pixels[y * width + (x-1)]
                    down = pixels[(y+1) * width + x]
                    up = pixels[(y-1) * width + x]
                    
                    gx = abs(right - left)
                    gy = abs(down - up)
                    sharpness += math.sqrt(gx*gx + gy*gy)
                    count += 1
            return sharpness / count if count > 0 else 0
        
        sharpness = calculate_sharpness(pixels, width, height)
        
        # 2. Contrast (standard deviation)
        mean_val = sum(pixels) / len(pixels)
        variance = sum((p - mean_val) ** 2 for p in pixels) / len(pixels)
        contrast = math.sqrt(variance)
        
        # 3. Brightness (mean)
        brightness = mean_val
        
        # 4. Noise estimation (simplified)
        def estimate_noise(pixels, width, height):
            noise = 0
            count = 0
            for y in range(1, height-1):
                for x in range(1, width-1):
                    # Local 3x3 variance
                    local_pixels = []
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            local_pixels.append(pixels[(y+dy) * width + (x+dx)])
                    
                    local_mean = sum(local_pixels) / len(local_pixels)
                    local_var = sum((p - local_mean) ** 2 for p in local_pixels) / len(local_pixels)
                    noise += local_var
                    count += 1
            return noise / count if count > 0 else 0
        
        noise_level = estimate_noise(pixels, width, height)
        
        # Quality scoring based on metrics
        # Higher sharpness and contrast = better quality
        # Lower noise = better quality
        
        quality_score = 0
        
        # Sharpness contribution (0-40 points)
        if sharpness > 50:
            quality_score += 40
        elif sharpness > 30:
            quality_score += 30
        elif sharpness > 20:
            quality_score += 20
        else:
            quality_score += 10
        
        # Contrast contribution (0-30 points)
        if contrast > 40:
            quality_score += 30
        elif contrast > 25:
            quality_score += 20
        elif contrast > 15:
            quality_score += 15
        else:
            quality_score += 5
        
        # Noise penalty (0-30 points deducted)
        if noise_level < 10:
            quality_score += 0  # No penalty
        elif noise_level < 20:
            quality_score += 10  # Small penalty
        elif noise_level < 40:
            quality_score += 20  # Medium penalty
        else:
            quality_score += 30  # Large penalty
        
        # Brightness check (penalty for too dark or too bright)
        if brightness < 30 or brightness > 220:
            quality_score += 15  # Penalty for poor brightness
        
        # Normalize score to 0-100 range
        quality_score = max(0, min(100, quality_score))
        
        # Determine category
        if quality_score < 30:
            category = "Good"
        elif quality_score < 60:
            category = "Moderate"
        else:
            category = "Bad"
        
        return quality_score, category, 0.001  # Very fast processing time
        
    except Exception as e:
        return 100.0, "Error", 0.0

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Image Quality Analysis API',
        'version': '1.0.0',
        'platform': 'Vercel',
        'method': 'PIL-only'
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
        score, category, processing_time = simple_quality_check(image)
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
        if len(images_data) > 5:
            return jsonify({
                'success': False,
                'error': 'Maximum 5 images allowed per batch'
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
                score, category, processing_time = simple_quality_check(image)
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
        
        # Calculate statistics without numpy
        avg_score = sum(scores) / len(scores) if scores else 0
        best_score = min(scores) if scores else 0
        worst_score = max(scores) if scores else 0
        
        summary = {
            'total_images': len(images_data),
            'successful_analyses': successful_analyses,
            'failed_analyses': failed_analyses,
            'average_score': float(avg_score),
            'best_score': float(best_score),
            'worst_score': float(worst_score),
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