# 🚀 Vercel Deployment Guide

## 🎯 Overview

This guide will help you deploy your Image Quality Analysis API to Vercel. Vercel supports Python serverless functions, making it perfect for your Flask API.

## ⚠️ Important Considerations

### **Vercel Limitations:**
- **Execution Time**: 10 seconds for Hobby plan, 60 seconds for Pro
- **Memory**: 1024MB for Hobby plan, 3008MB for Pro
- **File Size**: 50MB for Hobby plan, 100MB for Pro
- **Cold Starts**: First request may be slower
- **Dependencies**: Some heavy libraries may not work

### **Optimizations Made:**
- ✅ Simplified image processing for faster execution
- ✅ Limited batch size to 10 images
- ✅ Optimized memory usage
- ✅ Fallback implementation for missing dependencies

## 🚀 Deployment Steps

### **Step 1: Install Vercel CLI**

```bash
# Install Vercel CLI globally
npm install -g vercel

# Or use npx (no installation needed)
npx vercel
```

### **Step 2: Login to Vercel**

```bash
vercel login
```

### **Step 3: Deploy from Project Directory**

```bash
# Navigate to your project
cd /Users/marifatmaruf/Documents/IL-NIQE

# Deploy to Vercel
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name: il-niqe-api (or your preferred name)
# - Directory: ./
# - Override settings? N
```

### **Step 4: Configure Environment Variables (Optional)**

```bash
# Set environment variables if needed
vercel env add API_KEY
vercel env add DEBUG_MODE
```

### **Step 5: Deploy to Production**

```bash
# Deploy to production
vercel --prod
```

## 🔧 Configuration Files

### **vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

### **requirements.txt**
```
Flask==2.3.3
Flask-Cors==4.0.0
opencv-python==4.8.1.78
numpy==1.24.3
Pillow==10.0.1
scipy==1.11.3
requests==2.31.0
```

## 📱 API Endpoints

After deployment, your API will be available at:
- **Base URL**: `https://your-project-name.vercel.app`
- **Health Check**: `GET /health`
- **Single Analysis**: `POST /analyze-single`
- **Batch Analysis**: `POST /analyze-batch`

### **Example Usage:**

```bash
# Health check
curl https://your-project-name.vercel.app/health

# Single image analysis
curl -X POST https://your-project-name.vercel.app/analyze-single \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

## 🔄 Update Your Apps

### **Next.js Integration:**
```env
# .env.local
NEXT_PUBLIC_API_URL=https://your-project-name.vercel.app
```

### **Flutter Integration:**
```dart
// Update your Flutter app
static const String baseUrl = 'https://your-project-name.vercel.app';
```

## 🧪 Testing Deployment

### **Test Script for Vercel:**
```python
import requests
import base64

# Test Vercel deployment
API_URL = "https://your-project-name.vercel.app"

# Health check
response = requests.get(f"{API_URL}/health")
print("Health:", response.json())

# Test with sample image (you'll need to provide base64)
# response = requests.post(f"{API_URL}/analyze-single", 
#                         json={"image": "your_base64_image"})
# print("Analysis:", response.json())
```

## 🐛 Troubleshooting

### **Common Issues:**

#### 1. **Import Errors**
```python
# If optimized_quality_check fails to import
# The API will use a fallback implementation
```

#### 2. **Timeout Issues**
```python
# Reduce batch size or image size
# Vercel has execution time limits
```

#### 3. **Memory Issues**
```python
# Optimize image processing
# Use smaller image sizes
```

#### 4. **Cold Start Delays**
```python
# First request may take longer
# Consider using Vercel Pro for better performance
```

### **Debug Mode:**
```bash
# Check deployment logs
vercel logs

# Check function logs
vercel logs --follow
```

## 📊 Performance Optimization

### **For Better Performance:**

1. **Image Optimization:**
   - Resize images before sending
   - Use JPEG instead of PNG when possible
   - Compress images

2. **Batch Processing:**
   - Limit batch size to 5-10 images
   - Process images sequentially

3. **Caching:**
   - Use Vercel's edge caching
   - Cache results when possible

## 🔄 Alternative Deployment Options

### **Option 1: Railway**
```bash
# Deploy to Railway (better for Python)
railway login
railway init
railway up
```

### **Option 2: Render**
```bash
# Deploy to Render
# Create render.yaml and deploy
```

### **Option 3: Heroku**
```bash
# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

## 🎯 Production Considerations

### **Security:**
- Add API key authentication
- Implement rate limiting
- Validate input data

### **Monitoring:**
- Use Vercel Analytics
- Monitor function execution time
- Set up error alerts

### **Scaling:**
- Consider Vercel Pro for better limits
- Implement caching strategies
- Optimize for cold starts

## 🎉 Deployment Complete!

### **What You Get:**
✅ **Serverless API** - No server management needed  
✅ **Global CDN** - Fast worldwide access  
✅ **Auto-scaling** - Handles traffic spikes  
✅ **HTTPS** - Secure by default  
✅ **Easy Updates** - Deploy with one command  

### **Next Steps:**
1. **Test your deployed API**
2. **Update your apps** with the new URL
3. **Monitor performance** and usage
4. **Optimize** based on real usage

Your Image Quality Analysis API is now live on Vercel! 🚀

---

## 📞 Support

### **Vercel Documentation:**
- [Vercel Python Functions](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Vercel Limits](https://vercel.com/docs/limits)

### **Troubleshooting:**
- Check Vercel logs: `vercel logs`
- Test locally: `vercel dev`
- Monitor usage in Vercel dashboard
