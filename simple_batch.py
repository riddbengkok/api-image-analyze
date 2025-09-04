#!/usr/bin/env python3
"""
Simple IL-NIQE Batch Analyzer
Quick and easy batch image quality analysis
"""

import cv2
import os
import time
import importlib.util
spec = importlib.util.spec_from_file_location("ilniqe", "IL-NIQE.py")
ilniqe_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ilniqe_module)
calculate_ilniqe = ilniqe_module.calculate_ilniqe

def analyze_folder(folder_path, model_version='python'):
    """
    Simple batch analysis of all images in a folder
    
    Args:
        folder_path (str): Path to folder containing images
        model_version (str): 'python' or 'matlab'
    
    Returns:
        list: List of (filename, quality_score, category) tuples
    """
    print(f"🔍 Analyzing images in: {folder_path}")
    print("-" * 50)
    
    # Supported image extensions
    extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.PNG', '.JPG', '.JPEG')
    
    # Get all image files
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
            # Load and analyze image
            img = cv2.imread(img_path)
            if img is None:
                print(f"  ❌ Failed to load image")
                continue
            
            start_time = time.time()
            score = calculate_ilniqe(img, crop_border=0, input_order='HWC', 
                                   resize=True, version=model_version)
            process_time = time.time() - start_time
            
            # Categorize quality
            if score < 20:
                category = "Excellent"
            elif score < 40:
                category = "Good"
            elif score < 60:
                category = "Moderate"
            elif score < 80:
                category = "Poor"
            else:
                category = "Very Poor"
            
            results.append((filename, round(score, 2), category, round(process_time, 2)))
            print(f"  ✅ Score: {score:.2f} ({category}) - {process_time:.2f}s")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append((filename, None, "Error", 0))
        
        print()
    
    total_time = time.time() - total_start
    print(f"🎯 Total time: {total_time:.2f} seconds")
    
    return results

def print_summary(results):
    """Print a summary of the analysis results"""
    if not results:
        print("❌ No results to summarize")
        return
    
    print("\n📊 SUMMARY REPORT")
    print("=" * 50)
    
    # Filter successful results
    successful = [r for r in results if r[1] is not None]
    failed = [r for r in results if r[1] is None]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        scores = [r[1] for r in successful]
        categories = [r[2] for r in successful]
        
        print(f"\n📈 Quality Scores:")
        print(f"   Average: {sum(scores)/len(scores):.2f}")
        print(f"   Best:    {min(scores):.2f}")
        print(f"   Worst:   {max(scores):.2f}")
        
        print(f"\n📋 Quality Distribution:")
        for category in ["Excellent", "Good", "Moderate", "Poor", "Very Poor"]:
            count = categories.count(category)
            if count > 0:
                print(f"   {category}: {count} images")
    
    print(f"\n📋 DETAILED RESULTS:")
    print("-" * 60)
    print(f"{'Filename':<20} {'Score':<8} {'Category':<12} {'Time(s)':<8}")
    print("-" * 60)
    
    for filename, score, category, time_taken in results:
        score_str = f"{score:.2f}" if score is not None else "ERROR"
        print(f"{filename:<20} {score_str:<8} {category:<12} {time_taken:<8}")

def main():
    """Run batch analysis on pepper example images"""
    
    # Analyze the pepper example folder
    results = analyze_folder('./pepper_exa/', model_version='python')
    
    # Print summary
    print_summary(results)
    
    print(f"\n💡 Quality Guide:")
    print(f"   < 20:  Excellent (very natural)")
    print(f"   20-40: Good (minor distortions)")
    print(f"   40-60: Moderate (noticeable distortions)")
    print(f"   60-80: Poor (significant distortions)")
    print(f"   > 80:  Very Poor (heavy artifacts)")

if __name__ == "__main__":
    main()
