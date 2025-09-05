#!/usr/bin/env python3
"""
Image Quality Analysis API for Vercel
Using simple HTTP handler instead of Flask for better compatibility
"""

import json
import base64
import io
import time
import math
from http.server import BaseHTTPRequestHandler
from PIL import Image

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

def simple_quality_check(image, resize_dim=(200, 200)):
    """Simple image quality check using PIL only"""
    try:
        # Resize image for faster processing
        image_resized = image.resize(resize_dim, Image.Resampling.LANCZOS)
        
        # Convert to grayscale
        gray_image = image_resized.convert('L')
        
        # Get pixel data
        pixels = list(gray_image.getdata())
        width, height = gray_image.size
        
        # Calculate basic metrics
        
        # 1. Brightness (mean)
        brightness = sum(pixels) / len(pixels)
        
        # 2. Contrast (standard deviation)
        variance = sum((p - brightness) ** 2 for p in pixels) / len(pixels)
        contrast = math.sqrt(variance)
        
        # 3. Sharpness (simplified edge detection)
        sharpness = 0
        count = 0
        for y in range(1, height-1):
            for x in range(1, width-1):
                center = pixels[y * width + x]
                right = pixels[y * width + (x+1)]
                down = pixels[(y+1) * width + x]
                
                gx = abs(right - center)
                gy = abs(down - center)
                sharpness += math.sqrt(gx*gx + gy*gy)
                count += 1
        
        sharpness = sharpness / count if count > 0 else 0
        
        # 4. Simple quality scoring
        quality_score = 0
        
        # Brightness check (penalty for too dark or too bright)
        if 50 <= brightness <= 200:
            quality_score += 20
        elif 30 <= brightness <= 220:
            quality_score += 10
        
        # Contrast contribution
        if contrast > 30:
            quality_score += 30
        elif contrast > 20:
            quality_score += 20
        elif contrast > 10:
            quality_score += 10
        
        # Sharpness contribution
        if sharpness > 20:
            quality_score += 30
        elif sharpness > 15:
            quality_score += 20
        elif sharpness > 10:
            quality_score += 10
        
        # Normalize to 0-100 range
        quality_score = max(0, min(100, quality_score))
        
        # Determine category (FIXED: High scores = Good quality)
        if quality_score >= 60:
            category = "Good"      # High scores = Good (high contrast, sharp, well-lit)
        elif quality_score >= 30:
            category = "Moderate"  # Medium scores = Moderate
        else:
            category = "Bad"       # Low scores = Bad (blurry, low contrast, dark/bright)
        
        return quality_score, category, 0.001
        
    except Exception as e:
        return 100.0, "Error", 0.0

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'service': 'Image Quality Analysis API',
                'version': '3.0.0',
                'platform': 'Vercel',
                'method': 'HTTP Handler'
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        if self.path == '/analyze-single':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON
                data = json.loads(post_data.decode('utf-8'))
                
                if not data or 'image' not in data:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': 'No image data provided'
                    }).encode())
                    return
                
                # Convert base64 to image
                image = base64_to_image(data['image'])
                
                # Analyze image quality
                start_time = time.time()
                score, category, processing_time = simple_quality_check(image)
                total_time = time.time() - start_time
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': True,
                    'quality_score': float(score),
                    'category': category,
                    'processing_time': float(processing_time),
                    'total_time': float(total_time),
                    'timestamp': time.time()
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': str(e)
                }).encode())
        
        elif self.path == '/analyze-batch':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON
                data = json.loads(post_data.decode('utf-8'))
                
                if not data or 'images' not in data:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': 'No images data provided'
                    }).encode())
                    return
                
                images_data = data['images']
                if not isinstance(images_data, list) or len(images_data) == 0:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': 'Images must be a non-empty array'
                    }).encode())
                    return
                
                # Limit batch size for Vercel
                if len(images_data) > 3:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'success': False,
                        'error': 'Maximum 3 images allowed per batch'
                    }).encode())
                    return
                
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
                
                # Calculate statistics
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
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': True,
                    'results': results,
                    'summary': summary,
                    'timestamp': time.time()
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': str(e)
                }).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()