#!/usr/bin/env python3
"""
Fast Image Quality Checker
Simplified version of IL-NIQE for quick good/bad classification
"""

import cv2
import numpy as np
import time
import os
from scipy.ndimage import convolve
from scipy.signal import convolve2d

def matlab_fspecial(shape=(3,3), sigma=0.5):
    """2D gaussian mask"""
    m, n = [(ss-1.)/2. for ss in shape]
    y, x = np.ogrid[-m:m+1, -n:n+1]
    h = np.exp(-(x*x + y*y) / (2.*sigma*sigma))
    h[h < np.finfo(h.dtype).eps*h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def fast_quality_check(img, resize_factor=0.5):
    """
    Fast quality check using simplified features
    
    Args:
        img: Input image (BGR format)
        resize_factor: Factor to resize image for speed (0.5 = half size)
    
    Returns:
        tuple: (quality_score, category, processing_time)
    """
    start_time = time.time()
    
    # Convert to RGB and resize for speed
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]
    
    # Resize for faster processing
    new_h, new_w = int(h * resize_factor), int(w * resize_factor)
    img_small = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
    img_small = img_small.astype(np.float64)
    
    # Convert to grayscale for faster processing
    gray = 0.299 * img_small[:,:,0] + 0.587 * img_small[:,:,1] + 0.114 * img_small[:,:,2]
    
    # Simple quality indicators
    quality_score = 0
    
    # 1. Blur detection (Laplacian variance)
    laplacian_var = cv2.Laplacian(gray.astype(np.uint8), cv2.CV_64F).var()
    if laplacian_var < 100:  # Very blurry
        quality_score += 30
    elif laplacian_var < 500:  # Moderately blurry
        quality_score += 15
    
    # 2. Noise detection (standard deviation of gradients)
    grad_x = cv2.Sobel(gray.astype(np.uint8), cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray.astype(np.uint8), cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    noise_level = np.std(gradient_magnitude)
    
    if noise_level > 50:  # High noise
        quality_score += 25
    elif noise_level > 30:  # Moderate noise
        quality_score += 10
    
    # 3. Contrast check
    contrast = np.std(gray)
    if contrast < 30:  # Low contrast
        quality_score += 20
    elif contrast < 50:  # Moderate contrast
        quality_score += 10
    
    # 4. Brightness check
    brightness = np.mean(gray)
    if brightness < 30 or brightness > 225:  # Too dark or too bright
        quality_score += 15
    
    # 5. Color saturation check (simplified)
    color_std = np.std(img_small, axis=2)
    if np.mean(color_std) < 20:  # Low color variation
        quality_score += 10
    
    processing_time = time.time() - start_time
    
    # Categorize
    if quality_score < 15:
        category = "Good"
    elif quality_score < 35:
        category = "Moderate"
    else:
        category = "Bad"
    
    return quality_score, category, processing_time

def ultra_fast_check(img):
    """
    Ultra-fast quality check using only essential features
    ~0.1-0.5 seconds per image
    """
    start_time = time.time()
    
    # Convert to grayscale and resize
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA)
    
    quality_score = 0
    
    # 1. Blur check (Laplacian variance)
    laplacian_var = cv2.Laplacian(gray_small, cv2.CV_64F).var()
    if laplacian_var < 200:
        quality_score += 20
    
    # 2. Contrast check
    contrast = np.std(gray_small)
    if contrast < 40:
        quality_score += 15
    
    # 3. Brightness check
    brightness = np.mean(gray_small)
    if brightness < 40 or brightness > 215:
        quality_score += 10
    
    processing_time = time.time() - start_time
    
    # Simple categorization
    if quality_score < 10:
        category = "Good"
    elif quality_score < 25:
        category = "Moderate"
    else:
        category = "Bad"
    
    return quality_score, category, processing_time

def batch_fast_check(folder_path, method='ultra_fast'):
    """
    Fast batch analysis of images
    
    Args:
        folder_path: Path to folder containing images
        method: 'fast' or 'ultra_fast'
    """
    print(f"🚀 Fast Quality Check - Method: {method}")
    print(f"📁 Analyzing: {folder_path}")
    print("-" * 50)
    
    # Get image files
    extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.PNG', '.JPG', '.JPEG')
    image_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(extensions):
            image_files.append(os.path.join(folder_path, file))
    
    if not image_files:
        print("❌ No image files found!")
        return []
    
    print(f"📊 Found {len(image_files)} images")
    print()
    
    results = []
    total_start = time.time()
    
    for i, img_path in enumerate(image_files, 1):
        filename = os.path.basename(img_path)
        print(f"Processing {i}/{len(image_files)}: {filename}")
        
        try:
            img = cv2.imread(img_path)
            if img is None:
                print(f"  ❌ Failed to load")
                continue
            
            if method == 'ultra_fast':
                score, category, process_time = ultra_fast_check(img)
            else:
                score, category, process_time = fast_quality_check(img)
            
            results.append((filename, score, category, process_time))
            print(f"  ✅ Score: {score:.1f} ({category}) - {process_time:.3f}s")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append((filename, None, "Error", 0))
        
        print()
    
    total_time = time.time() - total_start
    print(f"🎯 Total time: {total_time:.2f} seconds")
    print(f"⚡ Average per image: {total_time/len(image_files):.3f} seconds")
    
    return results

def print_fast_summary(results):
    """Print summary of fast analysis"""
    if not results:
        print("❌ No results to summarize")
        return
    
    print("\n📊 FAST ANALYSIS SUMMARY")
    print("=" * 50)
    
    successful = [r for r in results if r[1] is not None]
    failed = [r for r in results if r[1] is None]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        scores = [r[1] for r in successful]
        categories = [r[2] for r in successful]
        times = [r[3] for r in successful]
        
        print(f"\n📈 Quality Scores:")
        print(f"   Average: {sum(scores)/len(scores):.1f}")
        print(f"   Best:    {min(scores):.1f}")
        print(f"   Worst:   {max(scores):.1f}")
        
        print(f"\n⏱️  Speed:")
        print(f"   Average: {sum(times)/len(times):.3f}s per image")
        print(f"   Total:   {sum(times):.2f}s")
        
        print(f"\n📋 Quality Distribution:")
        for category in ["Good", "Moderate", "Bad"]:
            count = categories.count(category)
            if count > 0:
                print(f"   {category}: {count} images")
    
    print(f"\n📋 RESULTS:")
    print("-" * 50)
    print(f"{'Filename':<20} {'Score':<6} {'Category':<10} {'Time(s)':<8}")
    print("-" * 50)
    
    for filename, score, category, time_taken in results:
        score_str = f"{score:.1f}" if score is not None else "ERROR"
        print(f"{filename:<20} {score_str:<6} {category:<10} {time_taken:<8}")

def main():
    """Test both fast methods"""
    
    print("🔥 SPEED COMPARISON TEST")
    print("=" * 60)
    
    # Test ultra-fast method
    print("\n1️⃣ ULTRA-FAST METHOD (~0.1-0.5s per image)")
    print("-" * 50)
    results_ultra = batch_fast_check('./pepper_exa/', method='ultra_fast')
    print_fast_summary(results_ultra)
    
    print("\n" + "="*60)
    
    # Test fast method
    print("\n2️⃣ FAST METHOD (~0.5-2s per image)")
    print("-" * 50)
    results_fast = batch_fast_check('./pepper_exa/', method='fast')
    print_fast_summary(results_fast)
    
    print(f"\n💡 SPEED IMPROVEMENT:")
    print(f"   Original IL-NIQE: ~16s per image")
    print(f"   Ultra-fast: ~0.1-0.5s per image (32-160x faster!)")
    print(f"   Fast: ~0.5-2s per image (8-32x faster!)")
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"   Use 'ultra_fast' for quick good/bad classification")
    print(f"   Use 'fast' for more detailed quality assessment")

if __name__ == "__main__":
    main()
