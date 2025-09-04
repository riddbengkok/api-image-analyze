# 🚀 Quick Reference Guide

## 📱 Flutter Integration Quick Start

### 1. Backend Setup (5 minutes)
```bash
# Install dependencies
pip3 install flask flask-cors opencv-python numpy pillow scipy

# Start server
python3 flask_api.py

# Test API
python3 test_api.py
```

### 2. Flutter Setup (10 minutes)
```yaml
# pubspec.yaml
dependencies:
  http: ^1.1.0
  image_picker: ^1.0.4
```

```dart
// Copy image_quality_service.dart to your lib/ folder
// Update server URL in the file
static const String _baseUrl = 'http://YOUR_IP:5000';
```

### 3. Basic Usage (2 minutes)
```dart
// Single image analysis
final result = await ImageQualityService.analyzeSingleImage(imageFile);
print('Quality: ${result.category} (${result.qualityScore})');

// Batch analysis
final batchResult = await ImageQualityService.analyzeBatchImages(imageFiles);
print('Average Score: ${batchResult.summary.averageScore}');
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analyze-single` | POST | Analyze single image |
| `/analyze-batch` | POST | Analyze multiple images |
| `/analyze-file` | POST | Analyze uploaded file |

## 📊 Response Format

### Single Image Analysis
```json
{
  "success": true,
  "quality_score": 45.0,
  "category": "Moderate",
  "processing_time": 0.004,
  "total_time": 0.123,
  "timestamp": 1234567890
}
```

### Batch Analysis
```json
{
  "success": true,
  "results": [
    {
      "index": 0,
      "quality_score": 45.0,
      "category": "Moderate",
      "processing_time": 0.004,
      "success": true
    }
  ],
  "summary": {
    "total_images": 3,
    "successful_analyses": 3,
    "failed_analyses": 0,
    "average_score": 46.4,
    "best_score": 42.0,
    "worst_score": 55.0,
    "category_distribution": {
      "Good": 0,
      "Moderate": 2,
      "Bad": 1
    },
    "total_processing_time": 0.234
  }
}
```

## 🎯 Quality Categories

| Score Range | Category | Description |
|-------------|----------|-------------|
| < 20 | Good | High quality, natural |
| 20-50 | Moderate | Acceptable quality |
| > 50 | Bad | Poor quality, distorted |

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Speed per image | ~0.004 seconds |
| Batch limit | 50 images |
| Image size limit | 10MB |
| Supported formats | JPG, PNG, BMP, TIFF |

## 🔧 Configuration

### Backend Configuration
```python
# flask_api.py
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Flutter Configuration
```dart
// image_quality_service.dart
static const String _baseUrl = 'http://YOUR_IP:5000';
static const Duration _timeout = Duration(seconds: 30);
```

## 🐛 Common Issues

### Server Connection Failed
```dart
// Check server status
final isHealthy = await ImageQualityService.isServerHealthy();
if (!isHealthy) {
  // Server is not running or not accessible
}
```

### Image Upload Failed
```dart
// Check image format
bool isValidImage(XFile image) {
  final extension = image.path.split('.').last.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'bmp'].contains(extension);
}
```

### Analysis Timeout
```dart
// Increase timeout
static const Duration _timeout = Duration(seconds: 60);
```

## 📱 Flutter Widget Examples

### Simple Image Picker
```dart
Future<void> pickAndAnalyze() async {
  final picker = ImagePicker();
  final image = await picker.pickImage(source: ImageSource.gallery);
  
  if (image != null) {
    final result = await ImageQualityService.analyzeSingleImage(image);
    print('Quality: ${result.category}');
  }
}
```

### Batch Image Analysis
```dart
Future<void> analyzeBatch() async {
  final picker = ImagePicker();
  final images = await picker.pickMultiImage();
  
  if (images.isNotEmpty) {
    final result = await ImageQualityService.analyzeBatchImages(images);
    print('Average Score: ${result.summary.averageScore}');
  }
}
```

### Error Handling
```dart
try {
  final result = await ImageQualityService.analyzeSingleImage(image);
  if (result.success) {
    // Handle success
    print('Quality: ${result.category}');
  } else {
    // Handle API error
    print('Error: ${result.error}');
  }
} catch (e) {
  // Handle network error
  print('Network error: $e');
}
```

## 🚀 Deployment

### Backend Deployment
```bash
# Heroku
heroku create your-app-name
git push heroku main

# Docker
docker build -t image-quality-api .
docker run -p 5000:5000 image-quality-api
```

### Flutter Deployment
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 📞 Support

### Debug Mode
```dart
// Enable debug logging
class ImageQualityService {
  static const bool _debugMode = true;
  
  static void _log(String message) {
    if (_debugMode) {
      print('[ImageQualityService] $message');
    }
  }
}
```

### Server Logs
```python
# flask_api.py
import logging
logging.basicConfig(level=logging.INFO)
```

### Common Commands
```bash
# Check server status
curl http://localhost:5000/health

# Test single image
python3 test_api.py

# Check Flutter dependencies
flutter pub get

# Run Flutter app
flutter run
```

## 🎯 Best Practices

1. **Always check server health** before analysis
2. **Handle errors gracefully** with user-friendly messages
3. **Show loading indicators** during analysis
4. **Cache results** to avoid re-analyzing same images
5. **Compress images** before sending for better performance
6. **Use appropriate timeout values** for your network
7. **Test on real devices** before production
8. **Monitor performance** and optimize as needed

## 📊 Monitoring

### Backend Metrics
```python
# Add to flask_api.py
@app.route('/metrics')
def get_metrics():
    return jsonify({
        'requests': metrics['requests'],
        'successful': metrics['successful_analyses'],
        'failed': metrics['failed_analyses'],
        'avg_time': metrics['average_processing_time']
    })
```

### Flutter Analytics
```dart
// Track usage
await _trackEvent('image_analysis', {
  'image_count': images.length,
  'avg_score': result.summary.averageScore,
  'processing_time': result.summary.totalProcessingTime
});
```

---

**Quick Start Time: ~15 minutes**  
**Perfect for: Mobile apps, batch processing, quality control**  
**Performance: 4000x faster than original IL-NIQE** 🚀
