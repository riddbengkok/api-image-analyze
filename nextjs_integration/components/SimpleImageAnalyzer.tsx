'use client';

import React, { useState } from 'react';
import { Upload, Play, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import ImageQualityService, { ImageQualityResult } from '../lib/imageQualityService';

const SimpleImageAnalyzer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<ImageQualityResult | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setResult(null); // Clear previous result
    }
  };

  const analyzeImage = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    try {
      const analysisResult = await ImageQualityService.analyzeSingleImage(selectedFile);
      setResult(analysisResult);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Good':
        return <CheckCircle className="w-6 h-6 text-green-600" />;
      case 'Moderate':
        return <AlertCircle className="w-6 h-6 text-orange-600" />;
      case 'Bad':
        return <XCircle className="w-6 h-6 text-red-600" />;
      default:
        return <AlertCircle className="w-6 h-6 text-gray-600" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Good':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'Moderate':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'Bad':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Simple Image Quality Analyzer
        </h1>
        <p className="text-gray-600">
          Upload an image to analyze its quality using advanced algorithms
        </p>
      </div>

      {/* File Upload */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Image
        </label>
        <div className="flex items-center space-x-4">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {selectedFile && (
            <button
              onClick={analyzeImage}
              disabled={isAnalyzing}
              className={`px-6 py-2 rounded-lg font-medium text-white flex items-center space-x-2 ${
                isAnalyzing
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {isAnalyzing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  <span>Analyze</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Image Preview */}
      {selectedFile && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Image Preview</h3>
          <div className="relative">
            <img
              src={URL.createObjectURL(selectedFile)}
              alt="Selected"
              className="w-full h-64 object-cover rounded-lg border border-gray-200"
            />
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-sm">
              {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
            </div>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {result && (
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Results</h3>
          
          {result.success ? (
            <div className="space-y-4">
              {/* Quality Score */}
              <div className="flex items-center justify-between p-4 bg-white rounded-lg border">
                <div>
                  <h4 className="font-medium text-gray-900">Quality Score</h4>
                  <p className="text-sm text-gray-600">Lower scores indicate better quality</p>
                </div>
                <div className="text-2xl font-bold text-blue-600">
                  {result.qualityScore.toFixed(1)}
                </div>
              </div>

              {/* Category */}
              <div className="flex items-center justify-between p-4 bg-white rounded-lg border">
                <div className="flex items-center space-x-3">
                  {getCategoryIcon(result.category)}
                  <div>
                    <h4 className="font-medium text-gray-900">Quality Category</h4>
                    <p className="text-sm text-gray-600">
                      {ImageQualityService.getCategoryDescription(result.category)}
                    </p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getCategoryColor(result.category)}`}>
                  {result.category}
                </span>
              </div>

              {/* Processing Time */}
              <div className="flex items-center justify-between p-4 bg-white rounded-lg border">
                <div>
                  <h4 className="font-medium text-gray-900">Processing Time</h4>
                  <p className="text-sm text-gray-600">Time taken to analyze the image</p>
                </div>
                <div className="text-lg font-semibold text-gray-700">
                  {result.processingTime.toFixed(3)}s
                </div>
              </div>

              {/* Quality Guide */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-medium text-blue-900 mb-2">Quality Guide</h4>
                <div className="space-y-1 text-sm text-blue-800">
                  <p>• <strong>Good (0-20):</strong> High quality, natural image</p>
                  <p>• <strong>Moderate (20-50):</strong> Acceptable quality with minor issues</p>
                  <p>• <strong>Bad (50+):</strong> Poor quality, significant distortions</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <XCircle className="w-5 h-5 text-red-600" />
                <span className="font-medium text-red-800">Analysis Failed</span>
              </div>
              <p className="text-red-700 mt-1">{result.error}</p>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div className="mt-8 bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 mb-2">How to Use</h4>
        <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
          <li>Click "Choose File" to select an image from your device</li>
          <li>Supported formats: JPG, PNG, BMP, TIFF</li>
          <li>Maximum file size: 10MB</li>
          <li>Click "Analyze" to start the quality assessment</li>
          <li>View the results including quality score and category</li>
        </ol>
      </div>
    </div>
  );
};

export default SimpleImageAnalyzer;
