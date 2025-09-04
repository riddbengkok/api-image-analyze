#!/bin/bash

# Script to deploy Image Quality Analysis API to Vercel

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

print_status "🚀 Starting Vercel deployment for Image Quality Analysis API..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_error "Vercel CLI is not installed. Please install it first:"
    echo "npm install -g vercel"
    echo "Or use: npx vercel"
    exit 1
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    print_warning "You are not logged in to Vercel. Please login first:"
    echo "vercel login"
    exit 1
fi

print_success "Vercel CLI is installed and you are logged in"

# Check if required files exist
required_files=("vercel.json" "api/index.py" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file not found: $file"
        exit 1
    fi
done

print_success "All required files are present"

# Deploy to Vercel
print_status "Deploying to Vercel..."
vercel --prod

print_success "🎉 Deployment completed successfully!"

print_status "Next steps:"
echo "1. Test your API: curl https://your-project-name.vercel.app/health"
echo "2. Update your Next.js app: NEXT_PUBLIC_API_URL=https://your-project-name.vercel.app"
echo "3. Update your Flutter app: baseUrl = 'https://your-project-name.vercel.app'"
echo "4. Check deployment logs: vercel logs"

print_success "Your Image Quality Analysis API is now live on Vercel! 🚀"
