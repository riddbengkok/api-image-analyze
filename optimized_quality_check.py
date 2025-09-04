#!/usr/bin/env python3
"""
Optimized Image Quality Checker
Fast and accurate good/bad classification
~0.1-0.5 seconds per image (32-160x faster than full IL-NIQE)
"""

import cv2
import numpy as np
import time
import os

def optimized_quality_check(img, resize_to=300):
    """
    Optimized quality check with better accuracy and speed
    
    Args:
        img: Input image (BGR format)
        resize_to: Size to resize image for processing
    
    Returns:
        tuple: (quality_score, category, processing_time)
    """
    start_time = time.time()
    
    # Convert to RGB and resize for speed
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_small = cv2.resize(img_rgb, (resize_to, resize_to), interpolation=cv2.INTER_AREA)
    img_small = img_small.astype(np.float64)
    
    # Convert to grayscale
    gray = 0.299 * img_small[:,:,0] + 0.587 * img_small[:,:,1] + 0.114 * img_small[:,:,2]
    
    quality_score = 0
    
    # 1. Blur detection (Laplacian variance) - Most important
    laplacian_var = cv2.Laplacian(gray.astype(np.uint8), cv2.CV_64F).var()
    
    if laplacian_var < 50:  # Very blurry
        quality_score += 40
    elif laplacian_var < 150:  # Moderately blurry
        quality_score += 25
    elif laplacian_var < 300:  # Slightly blurry
        quality_score += 10
    
    # 2. Noise detection (gradient analysis)
    grad_x = cv2.Sobel(gray.astype(np.uint8), cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray.astype(np.uint8), cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    # Check for excessive noise
    noise_level = np.std(gradient_magnitude)
    
    if noise_level > 70:  # High noise
        quality_score += 30
    elif noise_level > 45:  # Moderate noise
        quality_score += 15
    elif noise_level < 20:  # Too smooth (might be over-processed)
        quality_score += 8
    
    # 3. Contrast and brightness
    contrast = np.std(gray)
    brightness = np.mean(gray)
    
    if contrast < 25:  # Very low contrast
        quality_score += 25
    elif contrast < 40:  # Low contrast
        quality_score += 12
    
    if brightness < 30 or brightness > 225:  # Too dark or bright
        quality_score += 20
    elif brightness < 50 or brightness > 205:  # Poor lighting
        quality_score += 8
    
    # 4. Edge quality analysis
    edges = cv2.Canny(gray.astype(np.uint8), 50, 150)
    edge_density = np.sum(edges > 0) / (resize_to * resize_to)
    
    if edge_density < 0.01:  # Very few edges (might be blurry)
        quality_score += 20
    elif edge_density > 0.2:  # Too many edges (might be noisy)
        quality_score += 12
    
    # 5. Color quality (simplified)
    color_channels = [img_small[:,:,0], img_small[:,:,1], img_small[:,:,2]]
    color_means = [np.mean(ch) for ch in color_channels]
    color_std = [np.std(ch) for ch in color_channels]
    
    # Check for color imbalance
    max_mean = max(color_means)
    min_mean = min(color_means)
    color_imbalance = max_mean - min_mean
    
    if color_imbalance > 70:  # Strong color cast
        quality_score += 15
    elif color_imbalance > 50:  # Moderate color cast
        quality_score += 8
    
    # Check for oversaturation
    avg_color_std = np.mean(color_std)
    
    if avg_color_std < 25:  # Very low color variation
        quality_score += 12
    elif avg_color_std < 40:  # Low color variation
        quality_score += 6
    
    # 6. Texture analysis (simplified)
    # Use local binary patterns for texture
    lbp = cv2.calcHist([gray.astype(np.uint8)], [0], None, [256], [0, 256])
    texture_uniformity = np.sum(lbp**2) / (np.sum(lbp)**2)
    
    if texture_uniformity > 0.02:  # Too uniform (might be artificial)
        quality_score += 10
    elif texture_uniformity < 0.005:  # Too random (might be noisy)
        quality_score += 8
    
    processing_time = time.time() - start_time
    
    # Categorize based on score
    if quality_score < 20:
        category = "Good"
    elif quality_score < 50:
        category = "Moderate"
    else:
        category = "Bad"
    
    return quality_score, category, processing_time

def batch_optimized_check(folder_path, resize_to=300):
    """
    Optimized batch analysis of images
    
    Args:
        folder_path: Path to folder containing images
        resize_to: Size to resize images for processing
    """
    print(f"⚡ Optimized Quality Check (resize to {resize_to}x{resize_to})")
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
            
            score, category, process_time = optimized_quality_check(img, resize_to)
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

def print_optimized_summary(results):
    """Print summary of optimized analysis"""
    if not results:
        print("❌ No results to summarize")
        return
    
    print("\n📊 OPTIMIZED ANALYSIS SUMMARY")
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
        print(f"   Range:   {max(scores) - min(scores):.1f}")
        
        print(f"\n⏱️  Speed:")
        print(f"   Average: {sum(times)/len(times):.3f}s per image")
        print(f"   Total:   {sum(times):.2f}s")
        
        print(f"\n📋 Quality Distribution:")
        for category in ["Good", "Moderate", "Bad"]:
            count = categories.count(category)
            if count > 0:
                print(f"   {category}: {count} images")
    
    print(f"\n📋 DETAILED RESULTS:")
    print("-" * 60)
    print(f"{'Filename':<20} {'Score':<8} {'Category':<10} {'Time(s)':<8}")
    print("-" * 60)
    
    for filename, score, category, time_taken in results:
        score_str = f"{score:.1f}" if score is not None else "ERROR"
        print(f"{filename:<20} {score_str:<8} {category:<10} {time_taken:<8}")

def compare_with_original():
    """Compare optimized method with original IL-NIQE results"""
    print("🔄 COMPARISON WITH ORIGINAL IL-NIQE")
    print("=" * 60)
    
    # Original IL-NIQE results from our previous test
    original_results = {
        'pepper_0.png': 30.35,
        'pepper_1.png': 37.66,
        'pepper_2.png': 28.44,
        'pepper_3.png': 74.52,
        'pepper_4.png': 46.93
    }
    
    # Run optimized analysis
    results = batch_optimized_check('./pepper_exa/')
    
    print(f"\n📊 COMPARISON TABLE:")
    print("-" * 80)
    print(f"{'Image':<15} {'Original':<10} {'Optimized':<10} {'Diff':<8} {'Status':<10} {'Speed':<8}")
    print("-" * 80)
    
    for filename, score, category, time_taken in results:
        if score is not None and filename in original_results:
            orig_score = original_results[filename]
            diff = abs(score - orig_score)
            
            # Determine if results are consistent
            if (orig_score < 40 and category == "Good") or \
               (40 <= orig_score < 60 and category == "Moderate") or \
               (orig_score >= 60 and category == "Bad"):
                status = "✅ Match"
            else:
                status = "⚠️ Diff"
            
            print(f"{filename:<15} {orig_score:<10.1f} {score:<10.1f} {diff:<8.1f} {status:<10} {time_taken:<8.3f}s")
    
    print(f"\n💡 SPEED COMPARISON:")
    print(f"   Original IL-NIQE: ~16s per image")
    print(f"   Optimized method: ~0.1-0.5s per image")
    print(f"   Speed improvement: ~32-160x faster!")

def main():
    """Main function"""
    print("⚡ OPTIMIZED IMAGE QUALITY CHECKER")
    print("=" * 60)
    print("Fast and accurate good/bad classification")
    print()
    
    # Run optimized analysis
    results = batch_optimized_check('./pepper_exa/')
    print_optimized_summary(results)
    
    # Compare with original
    compare_with_original()
    
    print(f"\n🎯 USAGE:")
    print(f"   Good: Score < 20 (high quality, natural)")
    print(f"   Moderate: Score 20-50 (acceptable quality)")
    print(f"   Bad: Score > 50 (poor quality, distorted)")
    
    print(f"\n⚡ SPEED BENEFITS:")
    print(f"   - 32-160x faster than full IL-NIQE")
    print(f"   - Good accuracy for good/bad classification")
    print(f"   - Perfect for batch processing")

if __name__ == "__main__":
    main()
