#!/usr/bin/env python3
"""
Test the live Vercel API deployment
"""

import requests
import base64
import os

def test_vercel_api():
    """Test the live Vercel API"""
    base_url = "https://api-image-analyze.vercel.app"
    
    print("🧪 Testing Live Vercel API")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check: healthy")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Platform: {data.get('platform', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test with a sample image from pepper_exa folder
    pepper_folder = "pepper_exa"
    if os.path.exists(pepper_folder):
        image_files = [f for f in os.listdir(pepper_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            # Test with first image
            test_image = os.path.join(pepper_folder, image_files[0])
            print(f"\n📸 Testing with: {image_files[0]}")
            
            try:
                # Read and encode image
                with open(test_image, 'rb') as f:
                    image_data = f.read()
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                
                # Test single image analysis
                payload = {"image": base64_image}
                response = requests.post(f"{base_url}/analyze-single", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Single analysis: {data.get('quality_score', 0):.1f} ({data.get('category', 'Unknown')})")
                    print(f"   Processing time: {data.get('processing_time', 0):.3f}s")
                else:
                    print(f"❌ Single analysis failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Single analysis error: {e}")
        else:
            print("❌ No test images found in pepper_exa folder")
    else:
        print("❌ pepper_exa folder not found")
    
    print("\n🎉 Vercel API testing completed!")

if __name__ == "__main__":
    test_vercel_api()
