#!/usr/bin/env python3
"""
Script to start the Flask API server on port 5001
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

from flask_api import app

if __name__ == '__main__':
    print("🚀 Starting IL-NIQE server on 0.0.0.0:5001 (accessible from mobile devices)...")
    print("📱 Ready for Flutter mobile app integration")
    print("🌐 API Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /analyze-single - Analyze single image")
    print("   POST /analyze-batch - Analyze multiple images")
    print("   POST /analyze-file - Analyze uploaded file")
    print()
    print("🔗 Server URL: http://localhost:5001")
    print("📱 Mobile URL: http://YOUR_IP:5001 (replace YOUR_IP with your computer's IP)")
    print()
    
    # Run the app on port 5001
    app.run(host='0.0.0.0', port=5001, debug=False)
