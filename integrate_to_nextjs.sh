#!/bin/bash

# Script untuk mengintegrasikan Image Quality Analysis ke Next.js project existing
# Usage: ./integrate_to_nextjs.sh /path/to/your/nextjs-project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if target directory is provided
if [ $# -eq 0 ]; then
    print_error "Please provide the path to your Next.js project"
    echo "Usage: $0 /path/to/your/nextjs-project"
    exit 1
fi

TARGET_DIR="$1"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    print_error "Target directory does not exist: $TARGET_DIR"
    exit 1
fi

# Check if it's a Next.js project
if [ ! -f "$TARGET_DIR/package.json" ]; then
    print_error "Target directory is not a Next.js project (package.json not found)"
    exit 1
fi

print_status "Starting integration to Next.js project: $TARGET_DIR"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p "$TARGET_DIR/lib"
mkdir -p "$TARGET_DIR/components"

# Copy files
print_status "Copying integration files..."

# Copy API service
if [ -f "INTEGRATION_FILES/lib/imageQualityService.ts" ]; then
    cp "INTEGRATION_FILES/lib/imageQualityService.ts" "$TARGET_DIR/lib/"
    print_success "Copied imageQualityService.ts"
else
    print_error "imageQualityService.ts not found"
    exit 1
fi

# Copy component
if [ -f "INTEGRATION_FILES/components/SimpleImageAnalyzer.tsx" ]; then
    cp "INTEGRATION_FILES/components/SimpleImageAnalyzer.tsx" "$TARGET_DIR/components/"
    print_success "Copied SimpleImageAnalyzer.tsx"
else
    print_error "SimpleImageAnalyzer.tsx not found"
    exit 1
fi

# Copy environment example
if [ -f "INTEGRATION_FILES/env.example" ]; then
    cp "INTEGRATION_FILES/env.example" "$TARGET_DIR/.env.local.example"
    print_success "Copied environment example"
else
    print_warning "Environment example not found"
fi

# Install dependencies
print_status "Installing required dependencies..."
cd "$TARGET_DIR"

# Check if dependencies are already installed
if npm list axios > /dev/null 2>&1 && npm list react-dropzone > /dev/null 2>&1 && npm list lucide-react > /dev/null 2>&1; then
    print_success "Dependencies already installed"
else
    print_status "Installing axios, react-dropzone, lucide-react..."
    npm install axios react-dropzone lucide-react
    print_success "Dependencies installed successfully"
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_status "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
    print_success "Created .env.local file"
else
    print_warning ".env.local already exists. Please add NEXT_PUBLIC_API_URL=http://localhost:5000 manually"
fi

# Create example page
print_status "Creating example page..."
cat > pages/image-quality-demo.tsx << 'EOF'
import React from 'react';
import Head from 'next/head';
import SimpleImageAnalyzer from '../components/SimpleImageAnalyzer';

export default function ImageQualityDemo() {
  return (
    <>
      <Head>
        <title>Image Quality Analysis Demo</title>
        <meta name="description" content="Demo page for image quality analysis" />
      </Head>

      <div className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-center mb-8">
            Image Quality Analysis Demo
          </h1>
          <SimpleImageAnalyzer />
        </div>
      </div>
    </>
  );
}
EOF

print_success "Created example page: pages/image-quality-demo.tsx"

# Create integration guide
print_status "Creating integration guide..."
cat > IMAGE_QUALITY_INTEGRATION.md << 'EOF'
# 🎯 Image Quality Analysis Integration

## ✅ Integration Complete!

Your Next.js project now has image quality analysis capabilities.

## 🚀 Quick Start

### 1. Start Backend Server
```bash
cd /Users/marifatmaruf/Documents/IL-NIQE
python3 flask_api.py
```

### 2. Start Next.js Development Server
```bash
npm run dev
```

### 3. Test Integration
- Open http://localhost:3000/image-quality-demo
- Upload an image
- Click "Analyze"
- View results!

## 📁 Files Added

- `lib/imageQualityService.ts` - API service
- `components/SimpleImageAnalyzer.tsx` - Analysis component
- `pages/image-quality-demo.tsx` - Demo page
- `.env.local` - Environment variables

## 🔧 Usage

### Basic Usage
```tsx
import SimpleImageAnalyzer from '../components/SimpleImageAnalyzer';

export default function YourPage() {
  return (
    <div>
      <h1>Your Page</h1>
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
    console.log('Quality Score:', result.qualityScore);
    console.log('Category:', result.category);
  }
};
```

## 🎯 Features

✅ Single Image Analysis  
✅ Quality Categories (Good/Moderate/Bad)  
✅ Fast Processing (~0.004s per image)  
✅ Modern UI  
✅ TypeScript Support  
✅ Error Handling  

## 🐛 Troubleshooting

1. **Server Connection Failed**
   - Check if backend is running: `python3 flask_api.py`
   - Verify API URL in `.env.local`

2. **File Upload Issues**
   - Check file format (JPG, PNG, BMP, TIFF)
   - Verify file size (max 10MB)

## 📚 Documentation

- [Complete Integration Guide](../INTEGRATE_EXISTING_NEXTJS.md)
- [Next.js Integration Guide](../NEXTJS_INTEGRATION_GUIDE.md)

## 🎉 Ready to Use!

Your Next.js app now has powerful image quality analysis capabilities! 🚀
EOF

print_success "Created integration guide: IMAGE_QUALITY_INTEGRATION.md"

# Final instructions
print_success "Integration completed successfully!"
echo ""
print_status "Next steps:"
echo "1. Start backend server: cd /Users/marifatmaruf/Documents/IL-NIQE && python3 flask_api.py"
echo "2. Start Next.js dev server: npm run dev"
echo "3. Test integration: http://localhost:3000/image-quality-demo"
echo ""
print_status "Files added to your project:"
echo "- lib/imageQualityService.ts"
echo "- components/SimpleImageAnalyzer.tsx"
echo "- pages/image-quality-demo.tsx"
echo "- .env.local"
echo "- IMAGE_QUALITY_INTEGRATION.md"
echo ""
print_success "Your Next.js project now has image quality analysis capabilities! 🎉"
