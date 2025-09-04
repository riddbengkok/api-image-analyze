#!/usr/bin/env python3
"""
Test script to analyze all images in pepper_exa folder using the Flask API
"""

import os
import base64
import requests
import json
import time
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:5001"
PEPPER_FOLDER = "/Users/marifatmaruf/Documents/IL-NIQE/pepper_exa"

def test_api_health():
    """Test if the API server is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health Check: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API Health Check Error: {e}")
        return False

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        print(f"❌ Error encoding {image_path}: {e}")
        return None

def analyze_single_image(image_path):
    """Analyze a single image using the API"""
    print(f"\n📸 Analyzing: {os.path.basename(image_path)}")
    
    # Convert image to base64
    base64_image = image_to_base64(image_path)
    if not base64_image:
        return None
    
    try:
        # Send request to API
        payload = {"image": base64_image}
        response = requests.post(
            f"{API_BASE_URL}/analyze-single",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = {
                    'filename': os.path.basename(image_path),
                    'quality_score': data['quality_score'],
                    'category': data['category'],
                    'processing_time': data['processing_time'],
                    'total_time': data['total_time']
                }
                print(f"   ✅ Score: {result['quality_score']:.2f} ({result['category']})")
                print(f"   ⏱️  Time: {result['processing_time']:.3f}s")
                return result
            else:
                print(f"   ❌ Analysis failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
        return None

def analyze_batch_images(image_paths):
    """Analyze multiple images in batch using the API"""
    print(f"\n🔄 Batch Analysis: {len(image_paths)} images")
    
    # Convert all images to base64
    base64_images = []
    for image_path in image_paths:
        base64_image = image_to_base64(image_path)
        if base64_image:
            base64_images.append(base64_image)
        else:
            print(f"   ⚠️  Skipping {os.path.basename(image_path)} (encoding failed)")
    
    if not base64_images:
        print("   ❌ No valid images to analyze")
        return None
    
    try:
        # Send batch request to API
        payload = {"images": base64_images}
        response = requests.post(
            f"{API_BASE_URL}/analyze-batch",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Batch analysis completed")
                print(f"   📊 Total images: {data['summary']['total_images']}")
                print(f"   ✅ Successful: {data['summary']['successful_analyses']}")
                print(f"   ❌ Failed: {data['summary']['failed_analyses']}")
                print(f"   📈 Average score: {data['summary']['average_score']:.2f}")
                print(f"   ⏱️  Total time: {data['summary']['total_processing_time']:.2f}s")
                
                # Show individual results
                print(f"\n📋 Individual Results:")
                for i, result in enumerate(data['results']):
                    filename = os.path.basename(image_paths[i]) if i < len(image_paths) else f"Image {i+1}"
                    if result['success']:
                        print(f"   {filename}: {result['quality_score']:.2f} ({result['category']}) - {result['processing_time']:.3f}s")
                    else:
                        print(f"   {filename}: ❌ {result.get('error', 'Failed')}")
                
                return data
            else:
                print(f"   ❌ Batch analysis failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
        return None

def get_image_files(folder_path):
    """Get all image files from the folder"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_ext = Path(file).suffix.lower()
            if file_ext in image_extensions:
                image_files.append(file_path)
    
    return sorted(image_files)

def main():
    """Main test function"""
    print("🧪 Testing Image Quality Analysis API")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API server is not healthy. Please check if the server is running.")
        return
    
    # Get image files
    image_files = get_image_files(PEPPER_FOLDER)
    if not image_files:
        print(f"\n❌ No image files found in {PEPPER_FOLDER}")
        return
    
    print(f"\n📁 Found {len(image_files)} images in pepper_exa folder:")
    for img in image_files:
        print(f"   - {os.path.basename(img)}")
    
    # Test single image analysis
    print(f"\n🔍 Testing Single Image Analysis")
    print("-" * 30)
    single_results = []
    for image_path in image_files:
        result = analyze_single_image(image_path)
        if result:
            single_results.append(result)
        time.sleep(0.5)  # Small delay between requests
    
    # Test batch analysis
    print(f"\n🔄 Testing Batch Analysis")
    print("-" * 30)
    batch_result = analyze_batch_images(image_files)
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 50)
    print(f"✅ API Health: OK")
    print(f"📁 Images found: {len(image_files)}")
    print(f"✅ Single analysis: {len(single_results)}/{len(image_files)} successful")
    print(f"✅ Batch analysis: {'OK' if batch_result else 'Failed'}")
    
    if single_results:
        scores = [r['quality_score'] for r in single_results]
        categories = [r['category'] for r in single_results]
        times = [r['processing_time'] for r in single_results]
        
        print(f"\n📈 Quality Scores:")
        print(f"   Average: {sum(scores)/len(scores):.2f}")
        print(f"   Best: {min(scores):.2f}")
        print(f"   Worst: {max(scores):.2f}")
        
        print(f"\n⏱️  Processing Times:")
        print(f"   Average: {sum(times)/len(times):.3f}s")
        print(f"   Fastest: {min(times):.3f}s")
        print(f"   Slowest: {max(times):.3f}s")
        
        print(f"\n📋 Quality Distribution:")
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        for cat, count in category_counts.items():
            print(f"   {cat}: {count} images")
    
    print(f"\n🎉 API testing completed!")

if __name__ == "__main__":
    main()
