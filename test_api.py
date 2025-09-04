#!/usr/bin/env python3
"""
Test script for Flask API
"""

import requests
import base64
import json
import time

def test_health_endpoint():
    """Test health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def image_to_base64(image_path):
    """Convert image to base64"""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_single_image_analysis():
    """Test single image analysis"""
    print("\n🔍 Testing single image analysis...")
    try:
        # Use one of the pepper images
        image_path = './pepper_exa/pepper_0.png'
        base64_image = image_to_base64(image_path)
        
        payload = {'image': base64_image}
        
        start_time = time.time()
        response = requests.post(
            'http://localhost:5000/analyze-single',
            json=payload,
            timeout=30
        )
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Single image analysis passed")
            print(f"   Quality Score: {result['quality_score']}")
            print(f"   Category: {result['category']}")
            print(f"   Processing Time: {result['processing_time']:.3f}s")
            print(f"   Total Time: {total_time:.3f}s")
            return True
        else:
            print(f"❌ Single image analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Single image analysis error: {e}")
        return False

def test_batch_image_analysis():
    """Test batch image analysis"""
    print("\n🔍 Testing batch image analysis...")
    try:
        # Use multiple pepper images
        image_paths = [
            './pepper_exa/pepper_0.png',
            './pepper_exa/pepper_1.png',
            './pepper_exa/pepper_2.png'
        ]
        
        base64_images = []
        for path in image_paths:
            base64_images.append(image_to_base64(path))
        
        payload = {'images': base64_images}
        
        start_time = time.time()
        response = requests.post(
            'http://localhost:5000/analyze-batch',
            json=payload,
            timeout=60
        )
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Batch image analysis passed")
            print(f"   Total Images: {result['summary']['total_images']}")
            print(f"   Successful: {result['summary']['successful_analyses']}")
            print(f"   Average Score: {result['summary']['average_score']:.1f}")
            print(f"   Total Time: {total_time:.3f}s")
            
            # Show individual results
            print("   Individual Results:")
            for i, img_result in enumerate(result['results']):
                if img_result['success']:
                    print(f"     Image {i+1}: {img_result['quality_score']:.1f} ({img_result['category']})")
                else:
                    print(f"     Image {i+1}: Error - {img_result.get('error', 'Unknown')}")
            
            return True
        else:
            print(f"❌ Batch image analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch image analysis error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Flask API for Image Quality Analysis")
    print("=" * 60)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ API server is not running. Please start it with:")
        print("   python3 flask_api.py")
        return
    
    # Test single image analysis
    test_single_image_analysis()
    
    # Test batch image analysis
    test_batch_image_analysis()
    
    print("\n🎯 API Testing Complete!")
    print("📱 Your Flutter app can now connect to this API")

if __name__ == "__main__":
    main()
