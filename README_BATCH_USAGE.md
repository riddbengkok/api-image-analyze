# IL-NIQE Batch Analysis Guide

## 🚀 Quick Start

### 1. Simple Batch Analysis
```bash
python3 simple_batch.py
```

### 2. Custom Folder Analysis
```python
from simple_batch import analyze_folder, print_summary

# Analyze any folder
results = analyze_folder('/path/to/your/images/')
print_summary(results)
```

## 📊 Understanding the Results

### Quality Score Interpretation
- **Lower scores = Better quality** (more natural)
- **Higher scores = Poorer quality** (more distorted)

### Quality Categories
- **< 20**: Excellent (very natural)
- **20-40**: Good (minor distortions) 
- **40-60**: Moderate (noticeable distortions)
- **60-80**: Poor (significant distortions)
- **> 80**: Very Poor (heavy artifacts)

## 📈 Example Results from pepper_exa/

| Image | Score | Category | Quality |
|-------|-------|----------|---------|
| pepper_2.png | 28.44 | Good | Best quality |
| pepper_0.png | 30.35 | Good | Second best |
| pepper_1.png | 37.66 | Good | Third best |
| pepper_4.png | 46.93 | Moderate | Noticeable distortions |
| pepper_3.png | 74.52 | Poor | Significant distortions |

## 🛠 Advanced Usage

### Custom Analysis Script
```python
import cv2
import os
from IL_NIQE import calculate_ilniqe

def analyze_custom_folder(folder_path):
    results = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            
            # Calculate quality score
            score = calculate_ilniqe(img, crop_border=0, input_order='HWC', resize=True)
            
            # Categorize
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
            
            results.append({
                'filename': filename,
                'score': score,
                'category': category
            })
            
            print(f"{filename}: {score:.2f} ({category})")
    
    return results

# Usage
results = analyze_custom_folder('./your_images/')
```

## ⚡ Performance Tips

1. **Processing Time**: ~15-17 seconds per image
2. **Memory Usage**: Moderate (processes 84x84 blocks)
3. **Batch Size**: Can handle hundreds of images
4. **File Formats**: Supports PNG, JPG, JPEG, BMP, TIFF

## 🎯 Use Cases

### 1. Image Quality Filtering
```python
def filter_by_quality(folder_path, threshold=40):
    """Filter images by quality threshold"""
    good_images = []
    bad_images = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(os.path.join(folder_path, filename))
            score = calculate_ilniqe(img, crop_border=0)
            
            if score < threshold:
                good_images.append(filename)
            else:
                bad_images.append(filename)
    
    return good_images, bad_images
```

### 2. Quality Ranking
```python
def rank_images_by_quality(folder_path):
    """Rank all images by quality (best to worst)"""
    results = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(os.path.join(folder_path, filename))
            score = calculate_ilniqe(img, crop_border=0)
            results.append((filename, score))
    
    # Sort by score (lower is better)
    results.sort(key=lambda x: x[1])
    
    return results
```

### 3. Quality Monitoring
```python
def monitor_image_quality(image_path):
    """Monitor quality of a single image"""
    img = cv2.imread(image_path)
    score = calculate_ilniqe(img, crop_border=0)
    
    if score < 20:
        status = "✅ Excellent"
    elif score < 40:
        status = "✅ Good"
    elif score < 60:
        status = "⚠️ Moderate"
    elif score < 80:
        status = "❌ Poor"
    else:
        status = "🚫 Very Poor"
    
    print(f"Quality Score: {score:.2f} - {status}")
    return score
```

## 🔧 Troubleshooting

### Common Issues
1. **Import Error**: Make sure you're in the correct directory
2. **Memory Error**: Process images in smaller batches
3. **Slow Processing**: Normal for high-quality analysis (~15s per image)

### File Format Support
- ✅ PNG, JPG, JPEG, BMP, TIFF
- ❌ GIF, WEBP (convert to PNG/JPG first)

## 📝 Notes

- The algorithm is **completely blind** - no reference image needed
- Results are consistent with human perception
- Lower scores indicate better, more natural images
- Processing time scales linearly with number of images
