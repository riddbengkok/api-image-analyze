#!/usr/bin/env python3
"""
IL-NIQE Batch Image Quality Analyzer
Analyzes multiple images and provides quality assessment reports
"""

import cv2
import os
import time
import pandas as pd
import numpy as np
from IL_NIQE import calculate_ilniqe
import matplotlib.pyplot as plt
from pathlib import Path

class ImageQualityAnalyzer:
    def __init__(self, model_version='python'):
        """
        Initialize the analyzer
        
        Args:
            model_version (str): 'python' or 'matlab' - which model to use
        """
        self.model_version = model_version
        self.results = []
        
    def analyze_single_image(self, image_path, crop_border=0):
        """
        Analyze a single image and return quality metrics
        
        Args:
            image_path (str): Path to the image
            crop_border (int): Pixels to crop from edges
            
        Returns:
            dict: Analysis results
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return {
                    'filename': os.path.basename(image_path),
                    'quality_score': None,
                    'status': 'Failed to load',
                    'processing_time': 0,
                    'image_size': None
                }
            
            # Record image info
            height, width = img.shape[:2]
            file_size = os.path.getsize(image_path)
            
            # Calculate quality score
            start_time = time.time()
            quality_score = calculate_ilniqe(
                img, 
                crop_border=crop_border, 
                input_order='HWC', 
                resize=True, 
                version=self.model_version
            )
            processing_time = time.time() - start_time
            
            # Determine quality category
            if quality_score < 20:
                quality_category = "Excellent"
            elif quality_score < 40:
                quality_category = "Good"
            elif quality_score < 60:
                quality_category = "Moderate"
            elif quality_score < 80:
                quality_category = "Poor"
            else:
                quality_category = "Very Poor"
            
            return {
                'filename': os.path.basename(image_path),
                'quality_score': round(quality_score, 4),
                'quality_category': quality_category,
                'status': 'Success',
                'processing_time': round(processing_time, 2),
                'image_size': f"{width}x{height}",
                'file_size_kb': round(file_size / 1024, 2)
            }
            
        except Exception as e:
            return {
                'filename': os.path.basename(image_path),
                'quality_score': None,
                'status': f'Error: {str(e)}',
                'processing_time': 0,
                'image_size': None
            }
    
    def analyze_batch(self, image_folder, file_extensions=('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        """
        Analyze all images in a folder
        
        Args:
            image_folder (str): Path to folder containing images
            file_extensions (tuple): Valid image file extensions
            
        Returns:
            list: List of analysis results
        """
        print(f"🔍 Analyzing images in: {image_folder}")
        print(f"📁 Looking for files with extensions: {file_extensions}")
        print("-" * 60)
        
        # Get all image files
        image_files = []
        for ext in file_extensions:
            image_files.extend(Path(image_folder).glob(f"*{ext}"))
            image_files.extend(Path(image_folder).glob(f"*{ext.upper()}"))
        
        if not image_files:
            print("❌ No image files found!")
            return []
        
        print(f"📊 Found {len(image_files)} images to analyze")
        print()
        
        # Analyze each image
        results = []
        total_start_time = time.time()
        
        for i, image_path in enumerate(image_files, 1):
            print(f"Processing {i}/{len(image_files)}: {image_path.name}")
            
            result = self.analyze_single_image(str(image_path))
            results.append(result)
            
            if result['status'] == 'Success':
                print(f"  ✅ Quality Score: {result['quality_score']} ({result['quality_category']})")
                print(f"  ⏱️  Time: {result['processing_time']}s")
            else:
                print(f"  ❌ {result['status']}")
            print()
        
        total_time = time.time() - total_start_time
        print(f"🎯 Batch analysis completed in {total_time:.2f} seconds")
        
        self.results = results
        return results
    
    def generate_report(self, output_file=None):
        """
        Generate a detailed analysis report
        
        Args:
            output_file (str): Optional path to save report
        """
        if not self.results:
            print("❌ No results to report. Run analyze_batch() first.")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.results)
        
        # Filter successful analyses
        successful_results = df[df['status'] == 'Success']
        
        if successful_results.empty:
            print("❌ No successful analyses to report.")
            return
        
        print("📊 BATCH ANALYSIS REPORT")
        print("=" * 50)
        
        # Summary statistics
        print(f"📈 Total Images Processed: {len(df)}")
        print(f"✅ Successful Analyses: {len(successful_results)}")
        print(f"❌ Failed Analyses: {len(df) - len(successful_results)}")
        print()
        
        # Quality score statistics
        scores = successful_results['quality_score'].values
        print("📊 QUALITY SCORE STATISTICS:")
        print(f"   Average Score: {np.mean(scores):.2f}")
        print(f"   Median Score:  {np.median(scores):.2f}")
        print(f"   Min Score:     {np.min(scores):.2f}")
        print(f"   Max Score:     {np.max(scores):.2f}")
        print(f"   Std Deviation: {np.std(scores):.2f}")
        print()
        
        # Quality category distribution
        print("📋 QUALITY CATEGORY DISTRIBUTION:")
        category_counts = successful_results['quality_category'].value_counts()
        for category, count in category_counts.items():
            percentage = (count / len(successful_results)) * 100
            print(f"   {category}: {count} images ({percentage:.1f}%)")
        print()
        
        # Processing time statistics
        times = successful_results['processing_time'].values
        print("⏱️  PROCESSING TIME STATISTICS:")
        print(f"   Average Time: {np.mean(times):.2f} seconds")
        print(f"   Total Time:   {np.sum(times):.2f} seconds")
        print()
        
        # Detailed results table
        print("📋 DETAILED RESULTS:")
        print("-" * 80)
        print(f"{'Filename':<20} {'Score':<8} {'Category':<10} {'Time(s)':<8} {'Size':<12}")
        print("-" * 80)
        
        for _, row in successful_results.iterrows():
            print(f"{row['filename']:<20} {row['quality_score']:<8} {row['quality_category']:<10} {row['processing_time']:<8} {row['image_size']:<12}")
        
        # Failed analyses
        failed_results = df[df['status'] != 'Success']
        if not failed_results.empty:
            print("\n❌ FAILED ANALYSES:")
            print("-" * 40)
            for _, row in failed_results.iterrows():
                print(f"{row['filename']}: {row['status']}")
        
        # Save to file if requested
        if output_file:
            df.to_csv(output_file, index=False)
            print(f"\n💾 Results saved to: {output_file}")
    
    def get_best_worst_images(self, n=3):
        """
        Get the best and worst quality images
        
        Args:
            n (int): Number of best/worst images to return
        """
        if not self.results:
            print("❌ No results available. Run analyze_batch() first.")
            return None, None
        
        successful_results = [r for r in self.results if r['status'] == 'Success']
        
        if not successful_results:
            print("❌ No successful analyses available.")
            return None, None
        
        # Sort by quality score (lower is better)
        sorted_results = sorted(successful_results, key=lambda x: x['quality_score'])
        
        best_images = sorted_results[:n]
        worst_images = sorted_results[-n:]
        
        print(f"🏆 TOP {n} BEST QUALITY IMAGES:")
        print("-" * 40)
        for i, img in enumerate(best_images, 1):
            print(f"{i}. {img['filename']} - Score: {img['quality_score']} ({img['quality_category']})")
        
        print(f"\n💥 TOP {n} WORST QUALITY IMAGES:")
        print("-" * 40)
        for i, img in enumerate(worst_images, 1):
            print(f"{i}. {img['filename']} - Score: {img['quality_score']} ({img['quality_category']})")
        
        return best_images, worst_images

def main():
    """Example usage of the batch analyzer"""
    
    # Initialize analyzer
    analyzer = ImageQualityAnalyzer(model_version='python')
    
    # Analyze the pepper example images
    print("🚀 Starting IL-NIQE Batch Analysis")
    print("=" * 50)
    
    # Analyze batch of images
    results = analyzer.analyze_batch('./pepper_exa/')
    
    if results:
        # Generate comprehensive report
        analyzer.generate_report('image_quality_report.csv')
        
        # Get best and worst images
        analyzer.get_best_worst_images(n=2)
        
        print("\n🎯 Analysis Complete!")
        print("💡 Remember: Lower scores = Better quality")

if __name__ == "__main__":
    main()
