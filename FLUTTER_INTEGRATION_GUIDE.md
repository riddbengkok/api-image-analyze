# 📱 Flutter Integration Guide - Image Quality Analysis

## 🎯 Overview

Panduan lengkap untuk mengintegrasikan analisis kualitas gambar IL-NIQE ke dalam aplikasi Flutter Anda.

## 🏗️ Architecture

```
Flutter App (Mobile) → HTTP API → Python Backend → IL-NIQE Algorithm
```

## 📋 Prerequisites

### Backend Requirements
- Python 3.8+
- Flask
- OpenCV
- NumPy
- SciPy

### Flutter Requirements
- Flutter SDK 2.17.0+
- Dart SDK
- Android Studio / Xcode

## 🚀 Setup Instructions

### 1. Backend Setup

#### Install Python Dependencies
```bash
cd /Users/marifatmaruf/Documents/IL-NIQE
pip install -r requirements.txt
```

#### Start Backend Server
```bash
python3 flask_api.py
```

Server akan berjalan di `http://localhost:5000`

### 2. Flutter Setup

#### Create New Flutter Project
```bash
flutter create your_image_quality_app
cd your_image_quality_app
```

#### Add Dependencies
Edit `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  image_picker: ^1.0.4
  cupertino_icons: ^1.0.2
```

#### Copy Integration Files
Copy file-file berikut ke project Flutter Anda:
- `lib/image_quality_service.dart`
- `lib/batch_image_analyzer.dart`
- `lib/main.dart` (atau modifikasi sesuai kebutuhan)

### 3. Configure Server URL

Edit `lib/image_quality_service.dart`:
```dart
static const String _baseUrl = 'http://YOUR_SERVER_IP:5000';
```

Ganti `YOUR_SERVER_IP` dengan IP address server Anda.

## 📱 Usage Examples

### 1. Single Image Analysis

```dart
import 'package:image_picker/image_picker.dart';
import 'image_quality_service.dart';

// Pick image
final ImagePicker picker = ImagePicker();
final XFile? image = await picker.pickImage(source: ImageSource.gallery);

if (image != null) {
  // Analyze image
  final result = await ImageQualityService.analyzeSingleImage(image);
  
  if (result.success) {
    print('Quality Score: ${result.qualityScore}');
    print('Category: ${result.category}');
    print('Processing Time: ${result.processingTime}s');
  } else {
    print('Error: ${result.error}');
  }
}
```

### 2. Batch Image Analysis

```dart
import 'package:image_picker/image_picker.dart';
import 'image_quality_service.dart';

// Pick multiple images
final ImagePicker picker = ImagePicker();
final List<XFile> images = await picker.pickMultiImage();

if (images.isNotEmpty) {
  // Analyze batch
  final result = await ImageQualityService.analyzeBatchImages(images);
  
  if (result.success) {
    print('Total Images: ${result.summary.totalImages}');
    print('Average Score: ${result.summary.averageScore}');
    print('Good Images: ${result.summary.categoryDistribution['Good']}');
    print('Moderate Images: ${result.summary.categoryDistribution['Moderate']}');
    print('Bad Images: ${result.summary.categoryDistribution['Bad']}');
  }
}
```

### 3. Integration with Existing App

```dart
class YourExistingWidget extends StatefulWidget {
  @override
  _YourExistingWidgetState createState() => _YourExistingWidgetState();
}

class _YourExistingWidgetState extends State<YourExistingWidget> {
  List<XFile> selectedImages = [];
  bool isAnalyzing = false;
  BatchAnalysisResult? analysisResult;

  Future<void> analyzeSelectedImages() async {
    setState(() {
      isAnalyzing = true;
    });

    try {
      final result = await ImageQualityService.analyzeBatchImages(selectedImages);
      setState(() {
        analysisResult = result;
        isAnalyzing = false;
      });
    } catch (e) {
      setState(() {
        isAnalyzing = false;
      });
      // Handle error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Your existing UI
          
          // Add analysis button
          ElevatedButton(
            onPressed: isAnalyzing ? null : analyzeSelectedImages,
            child: isAnalyzing 
              ? CircularProgressIndicator()
              : Text('Analyze Images'),
          ),
          
          // Show results
          if (analysisResult != null)
            Expanded(
              child: ListView.builder(
                itemCount: analysisResult!.results.length,
                itemBuilder: (context, index) {
                  final result = analysisResult!.results[index];
                  return ListTile(
                    title: Text('Image ${index + 1}'),
                    subtitle: Text('Score: ${result.qualityScore.toStringAsFixed(1)}'),
                    trailing: Chip(
                      label: Text(result.category),
                      backgroundColor: _getCategoryColor(result.category),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category) {
      case 'Good': return Colors.green;
      case 'Moderate': return Colors.orange;
      case 'Bad': return Colors.red;
      default: return Colors.grey;
    }
  }
}
```

## 🌐 Deployment Options

### Option 1: Local Development
- Backend: `python3 flask_api.py`
- Flutter: `flutter run`
- URL: `http://localhost:5000`

### Option 2: Cloud Deployment

#### Backend (Heroku/Railway/DigitalOcean)
```bash
# Deploy to Heroku
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

#### Flutter App
- Build APK: `flutter build apk`
- Build iOS: `flutter build ios`
- Deploy to stores

### Option 3: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "flask_api.py"]
```

#### Run with Docker
```bash
docker build -t image-quality-api .
docker run -p 5000:5000 image-quality-api
```

## 🔧 Configuration

### Backend Configuration
```python
# flask_api.py
app.run(host='0.0.0.0', port=5000, debug=False)  # Production
```

### Flutter Configuration
```dart
// image_quality_service.dart
static const String _baseUrl = 'https://your-api-domain.com';  // Production
```

## 📊 Performance Optimization

### Backend Optimization
```python
# Add caching
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/analyze-single', methods=['POST'])
@cache.memoize(timeout=300)  # Cache for 5 minutes
def analyze_single_image():
    # ... existing code
```

### Flutter Optimization
```dart
// Add image compression
import 'package:image/image.dart' as img;

Future<String> compressAndEncodeImage(XFile imageFile) async {
  final bytes = await imageFile.readAsBytes();
  final image = img.decodeImage(bytes);
  final resized = img.copyResize(image!, width: 800);  // Resize for faster processing
  final compressed = img.encodeJpg(resized, quality: 85);
  return base64Encode(compressed);
}
```

## 🛡️ Security Considerations

### Backend Security
```python
# Add rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/analyze-single', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_single_image():
    # ... existing code
```

### Flutter Security
```dart
// Add input validation
bool isValidImage(XFile image) {
  final extension = image.path.split('.').last.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'bmp'].contains(extension);
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Check server IP address
   - Verify server is running
   - Check firewall settings

2. **Image Upload Failed**
   - Check image format (JPG, PNG, BMP)
   - Verify image size (max 10MB recommended)
   - Check network connection

3. **Analysis Timeout**
   - Reduce image size
   - Check server performance
   - Increase timeout duration

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

## 📈 Monitoring

### Backend Monitoring
```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)

@app.route('/analyze-single', methods=['POST'])
def analyze_single_image():
    logging.info(f"Analyzing image from {request.remote_addr}")
    # ... existing code
```

### Flutter Monitoring
```dart
// Add analytics
import 'package:firebase_analytics/firebase_analytics.dart';

Future<void> _trackAnalysisEvent(int imageCount, double avgScore) async {
  await FirebaseAnalytics.instance.logEvent(
    name: 'image_quality_analysis',
    parameters: {
      'image_count': imageCount,
      'average_score': avgScore,
    },
  );
}
```

## 🎯 Best Practices

1. **Image Preprocessing**: Resize images before sending to reduce bandwidth
2. **Error Handling**: Always handle network errors gracefully
3. **Loading States**: Show loading indicators during analysis
4. **Caching**: Cache results to avoid re-analyzing same images
5. **Batch Size**: Limit batch size to 10-20 images for optimal performance

## 📞 Support

Jika mengalami masalah:
1. Check server logs
2. Verify network connectivity
3. Test with smaller images
4. Check Flutter console for errors

---

**Selamat!** Anda sekarang memiliki sistem analisis kualitas gambar yang terintegrasi dengan Flutter app Anda! 🎉
