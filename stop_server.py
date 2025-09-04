#!/usr/bin/env python3
"""
Script to stop the Flask API server
"""

import os
import signal
import subprocess

def stop_server():
    """Stop the Flask API server"""
    try:
        # Find and kill the Flask server process
        result = subprocess.run(['pkill', '-f', 'flask_api'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Flask API server stopped successfully")
        else:
            print("ℹ️  No Flask API server process found")
            
        # Also try to kill any Python processes running start_server.py
        result2 = subprocess.run(['pkill', '-f', 'start_server.py'], capture_output=True, text=True)
        
        if result2.returncode == 0:
            print("✅ Server startup script stopped")
            
    except Exception as e:
        print(f"❌ Error stopping server: {e}")

if __name__ == '__main__':
    print("🛑 Stopping IL-NIQE server...")
    stop_server()
    print("🎉 Server stopped!")
