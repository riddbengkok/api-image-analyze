# 📁 Integration Files for Existing Next.js Project

## 🎯 Overview

File-file ini siap untuk di-copy ke project Next.js existing Anda untuk mengintegrasikan analisis kualitas gambar IL-NIQE.

## 📋 Files Included

```
INTEGRATION_FILES/
├── lib/
│   └── imageQualityService.ts        # API service dengan TypeScript
├── components/
│   └── SimpleImageAnalyzer.tsx       # Simple component untuk analisis
├── package.json                      # Dependencies yang diperlukan
├── env.example                       # Environment variables example
└── README.md                         # File ini
```

## 🚀 Quick Integration Steps

### 1. Copy Files ke Project Next.js Anda

```bash
# Copy API service
cp INTEGRATION_FILES/lib/imageQualityService.ts /path/to/your/nextjs-project/lib/

# Copy component
cp INTEGRATION_FILES/components/SimpleImageAnalyzer.tsx /path/to/your/nextjs-project/components/
```

### 2. Install Dependencies

```bash
cd /path/to/your/nextjs-project
npm install axios react-dropzone lucide-react
```

### 3. Setup Environment Variables

```bash
# Copy environment example
cp INTEGRATION_FILES/env.example /path/to/your/nextjs-project/.env.local

# Edit .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
```

### 4. Start Backend Server

```bash
# Di direktori IL-NIQE
cd /Users/marifatmaruf/Documents/IL-NIQE
python3 flask_api.py
```

### 5. Use Component di Project Anda

```tsx
import SimpleImageAnalyzer from '../components/SimpleImageAnalyzer';

export default function YourPage() {
  return (
    <div>
      <h1>Your Existing Page</h1>
      <SimpleImageAnalyzer />
    </div>
  );
}
```

## 🔧 Configuration

### Environment Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Component Props (Optional)
```tsx
<SimpleImageAnalyzer 
  onAnalysisComplete={(result) => {
    console.log('Analysis completed:', result);
  }}
/>
```

## 🎯 Features

✅ **Single Image Analysis** - Upload dan analisis satu gambar  
✅ **Quality Categories** - Good/Moderate/Bad classification  
✅ **Fast Processing** - ~0.004 seconds per image  
✅ **Modern UI** - Beautiful, responsive interface  
✅ **TypeScript** - Full type safety  
✅ **Error Handling** - Robust error handling  

## 🐛 Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Pastikan backend server running: `python3 flask_api.py`
   - Check environment variable: `NEXT_PUBLIC_API_URL`

2. **File Upload Issues**
   - Check file format (JPG, PNG, BMP, TIFF)
   - Verify file size (max 10MB)

3. **Dependencies Issues**
   - Run: `npm install axios react-dropzone lucide-react`

## 📚 Documentation

- **[INTEGRATE_EXISTING_NEXTJS.md](../INTEGRATE_EXISTING_NEXTJS.md)** - Complete integration guide
- **[NEXTJS_INTEGRATION_GUIDE.md](../NEXTJS_INTEGRATION_GUIDE.md)** - Detailed documentation

## 🎉 Ready to Use!

Copy file-file ini ke project Next.js existing Anda dan Anda akan memiliki kemampuan analisis kualitas gambar yang powerful! 🚀
