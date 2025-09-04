#!/usr/bin/env python3
"""
Test script for Vercel API deployment
"""

import sys
import os
import base64
import requests
import time

# Add current directory to path
sys.path.append('.')

def test_vercel_api_locally():
    """Test the Vercel API configuration locally"""
    print("🧪 Testing Vercel API configuration locally...")
    
    try:
        from api.index import app
        
        # Test with Flask test client
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Health check: {data['status']}")
                print(f"   Service: {data['service']}")
                print(f"   Platform: {data['platform']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
            
            # Test analyze-single endpoint with dummy data
            dummy_payload = {
                "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="  # 1x1 pixel PNG
            }
            
            response = client.post('/analyze-single', json=dummy_payload)
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print(f"✅ Single analysis: {data['quality_score']} ({data['category']})")
                else:
                    print(f"❌ Single analysis failed: {data.get('error')}")
            else:
                print(f"❌ Single analysis request failed: {response.status_code}")
                return False
            
            # Test batch analysis
            batch_payload = {
                "images": [dummy_payload["image"], dummy_payload["image"]]
            }
            
            response = client.post('/analyze-batch', json=batch_payload)
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print(f"✅ Batch analysis: {data['summary']['total_images']} images processed")
                    print(f"   Average score: {data['summary']['average_score']:.2f}")
                else:
                    print(f"❌ Batch analysis failed: {data.get('error')}")
            else:
                print(f"❌ Batch analysis request failed: {response.status_code}")
                return False
        
        print("✅ All local tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Local test failed: {e}")
        return False

def test_vercel_deployment(vercel_url):
    """Test the deployed Vercel API"""
    print(f"🌐 Testing Vercel deployment: {vercel_url}")
    
    try:
        # Test health endpoint
        response = requests.get(f"{vercel_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Platform: {data['platform']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test analyze-single endpoint
        dummy_payload = {
            "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }
        
        response = requests.post(f"{vercel_url}/analyze-single", json=dummy_payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Single analysis: {data['quality_score']} ({data['category']})")
                print(f"   Processing time: {data['processing_time']:.3f}s")
            else:
                print(f"❌ Single analysis failed: {data.get('error')}")
        else:
            print(f"❌ Single analysis request failed: {response.status_code}")
            return False
        
        print("✅ All deployment tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Deployment test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Vercel API Testing")
    print("=" * 50)
    
    # Test locally first
    if not test_vercel_api_locally():
        print("\n❌ Local tests failed. Please fix issues before deploying.")
        return
    
    print("\n" + "=" * 50)
    print("✅ Local tests passed! Ready for deployment.")
    print("\n🚀 To deploy to Vercel:")
    print("1. Run: ./deploy_to_vercel.sh")
    print("2. Or manually: vercel --prod")
    print("\n📱 After deployment, update your apps:")
    print("Next.js: NEXT_PUBLIC_API_URL=https://your-project-name.vercel.app")
    print("Flutter: baseUrl = 'https://your-project-name.vercel.app'")
    
    # If a Vercel URL is provided as argument, test it
    if len(sys.argv) > 1:
        vercel_url = sys.argv[1]
        print(f"\n🌐 Testing deployed API: {vercel_url}")
        test_vercel_deployment(vercel_url)

if __name__ == "__main__":
    main()
