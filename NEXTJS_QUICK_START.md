# 🚀 Next.js Quick Start Guide

## ⚡ 10-Minute Setup

### 1. Backend Setup (2 minutes)
```bash
# Start Python backend
cd /Users/marifatmaruf/Documents/IL-NIQE
python3 flask_api.py
```

### 2. Next.js Setup (8 minutes)
```bash
# Create Next.js project
npx create-next-app@latest my-image-app --typescript --tailwind --eslint
cd my-image-app

# Install dependencies
npm install axios react-dropzone lucide-react

# Copy files
cp ../nextjs_integration/lib/imageQualityService.ts lib/
cp ../nextjs_integration/components/SimpleImageAnalyzer.tsx components/
cp ../nextjs_integration/pages/simple.tsx pages/

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local

# Start development server
npm run dev
```

### 3. Test (1 minute)
- Open http://localhost:3000/simple
- Upload an image
- Click "Analyze"
- View results!

## 📱 Usage Examples

### Simple Integration
```tsx
import SimpleImageAnalyzer from '../components/SimpleImageAnalyzer';

export default function Home() {
  return (
    <div>
      <h1>My App</h1>
      <SimpleImageAnalyzer />
    </div>
  );
}
```

### API Service Usage
```tsx
import ImageQualityService from '../lib/imageQualityService';

const analyzeImage = async (file: File) => {
  const result = await ImageQualityService.analyzeSingleImage(file);
  
  if (result.success) {
    console.log('Quality:', result.category);
    console.log('Score:', result.qualityScore);
  }
};
```

## 🎯 Features

✅ **Single Image Analysis** - Upload and analyze one image  
✅ **Quality Categories** - Good/Moderate/Bad classification  
✅ **Fast Processing** - ~0.004 seconds per image  
✅ **Modern UI** - Beautiful, responsive interface  
✅ **TypeScript** - Full type safety  
✅ **Error Handling** - Robust error handling  

## 🔧 Configuration

### Environment Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Customization
```tsx
// Customize the component
<SimpleImageAnalyzer 
  maxFileSize={5}  // 5MB limit
  onAnalysisComplete={(result) => {
    console.log('Analysis done:', result);
  }}
/>
```

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Check if backend is running: `python3 flask_api.py`
   - Verify API URL in `.env.local`

2. **File Upload Issues**
   - Check file format (JPG, PNG, BMP, TIFF)
   - Verify file size (max 10MB)

3. **Analysis Timeout**
   - Check network connection
   - Verify server performance

### Debug Mode
```tsx
// Enable debug logging
const DEBUG = process.env.NODE_ENV === 'development';
if (DEBUG) {
  console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
}
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Speed** | ~0.004s per image |
| **File Size** | Up to 10MB |
| **Formats** | JPG, PNG, BMP, TIFF |
| **Browser** | All modern browsers |

## 🎉 Ready to Go!

Your Next.js app now has powerful image quality analysis! 

**Next Steps:**
1. Customize the UI to match your brand
2. Add more features as needed
3. Deploy to production
4. Monitor usage and performance

**Perfect for:**
- Photo quality assessment
- Image filtering
- Content moderation
- Quality control systems

🚀 **Start analyzing images in minutes!**
