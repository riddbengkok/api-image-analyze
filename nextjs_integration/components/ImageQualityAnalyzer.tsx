'use client';

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Upload, 
  Image as ImageIcon, 
  Trash2, 
  Play, 
  CheckCircle, 
  AlertCircle, 
  XCircle,
  Loader2,
  BarChart3,
  Clock,
  TrendingUp
} from 'lucide-react';
import ImageQualityService, { 
  ImageQualityResult, 
  BatchAnalysisResult 
} from '../lib/imageQualityService';

interface ImageQualityAnalyzerProps {
  onAnalysisComplete?: (result: BatchAnalysisResult) => void;
  maxFiles?: number;
  maxFileSize?: number; // in MB
}

const ImageQualityAnalyzer: React.FC<ImageQualityAnalyzerProps> = ({
  onAnalysisComplete,
  maxFiles = 50,
  maxFileSize = 10
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isServerHealthy, setIsServerHealthy] = useState<boolean | null>(null);
  const [analysisResult, setAnalysisResult] = useState<BatchAnalysisResult | null>(null);

  // Check server health on component mount
  React.useEffect(() => {
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    const healthy = await ImageQualityService.isServerHealthy();
    setIsServerHealthy(healthy);
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = [...files, ...acceptedFiles].slice(0, maxFiles);
    setFiles(newFiles);
    setAnalysisResult(null); // Clear previous results
  }, [files, maxFiles]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    maxSize: maxFileSize * 1024 * 1024, // Convert MB to bytes
    multiple: true
  });

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
    setAnalysisResult(null);
  };

  const clearAllFiles = () => {
    setFiles([]);
    setAnalysisResult(null);
  };

  const analyzeImages = async () => {
    if (files.length === 0) {
      alert('Please select images first');
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await ImageQualityService.analyzeBatchImages(files);
      setAnalysisResult(result);
      onAnalysisComplete?.(result);
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
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'Moderate':
        return <AlertCircle className="w-4 h-4 text-orange-600" />;
      case 'Bad':
        return <XCircle className="w-4 h-4 text-red-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-600" />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Image Quality Analyzer
        </h1>
        <p className="text-gray-600">
          Analyze multiple images for quality assessment using advanced IL-NIQE algorithm
        </p>
      </div>

      {/* Server Status */}
      <div className={`p-4 rounded-lg border ${
        isServerHealthy === null 
          ? 'bg-gray-50 border-gray-200' 
          : isServerHealthy 
            ? 'bg-green-50 border-green-200' 
            : 'bg-red-50 border-red-200'
      }`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {isServerHealthy === null ? (
              <Loader2 className="w-5 h-5 text-gray-500 animate-spin" />
            ) : isServerHealthy ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : (
              <XCircle className="w-5 h-5 text-red-600" />
            )}
            <span className={`font-medium ${
              isServerHealthy === null 
                ? 'text-gray-700' 
                : isServerHealthy 
                  ? 'text-green-700' 
                  : 'text-red-700'
            }`}>
              {isServerHealthy === null 
                ? 'Checking server...' 
                : isServerHealthy 
                  ? 'Server Connected' 
                  : 'Server Disconnected'}
            </span>
          </div>
          <button
            onClick={checkServerHealth}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* File Upload Area */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        {isDragActive ? (
          <p className="text-lg text-blue-600">Drop the images here...</p>
        ) : (
          <div>
            <p className="text-lg text-gray-600 mb-2">
              Drag & drop images here, or click to select
            </p>
            <p className="text-sm text-gray-500">
              Supports JPG, PNG, BMP, TIFF (max {maxFileSize}MB each, up to {maxFiles} files)
            </p>
          </div>
        )}
      </div>

      {/* Selected Files */}
      {files.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Selected Images ({files.length})
            </h3>
            <button
              onClick={clearAllFiles}
              className="text-sm text-red-600 hover:text-red-800 font-medium flex items-center space-x-1"
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear All</span>
            </button>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {files.map((file, index) => (
              <div key={index} className="relative group">
                <div className="aspect-square rounded-lg overflow-hidden border border-gray-200">
                  <img
                    src={URL.createObjectURL(file)}
                    alt={file.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <XCircle className="w-4 h-4" />
                </button>
                <p className="text-xs text-gray-600 mt-1 truncate">
                  {file.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(1)} MB
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Analyze Button */}
      {files.length > 0 && (
        <div className="text-center">
          <button
            onClick={analyzeImages}
            disabled={isAnalyzing || !isServerHealthy}
            className={`px-8 py-3 rounded-lg font-medium text-white flex items-center space-x-2 mx-auto ${
              isAnalyzing || !isServerHealthy
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                <span>Analyze Images</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            <BarChart3 className="w-5 h-5" />
            <span>Analysis Results</span>
          </h3>

          {!analysisResult.success ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <XCircle className="w-5 h-5 text-red-600" />
                <span className="text-red-800 font-medium">Analysis Failed</span>
              </div>
              <p className="text-red-700 mt-1">{analysisResult.error}</p>
            </div>
          ) : (
            <>
              {/* Summary */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-blue-900 mb-3">Summary</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-blue-700 font-medium">Total Images</p>
                    <p className="text-blue-900 text-lg font-bold">
                      {analysisResult.summary.totalImages}
                    </p>
                  </div>
                  <div>
                    <p className="text-blue-700 font-medium">Successful</p>
                    <p className="text-blue-900 text-lg font-bold">
                      {analysisResult.summary.successfulAnalyses}
                    </p>
                  </div>
                  <div>
                    <p className="text-blue-700 font-medium">Average Score</p>
                    <p className="text-blue-900 text-lg font-bold">
                      {analysisResult.summary.averageScore.toFixed(1)}
                    </p>
                  </div>
                  <div>
                    <p className="text-blue-700 font-medium">Processing Time</p>
                    <p className="text-blue-900 text-lg font-bold flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>{analysisResult.summary.totalProcessingTime.toFixed(2)}s</span>
                    </p>
                  </div>
                </div>

                {/* Quality Distribution */}
                <div className="mt-4">
                  <p className="text-blue-700 font-medium mb-2">Quality Distribution</p>
                  <div className="flex space-x-4">
                    {Object.entries(analysisResult.summary.categoryDistribution).map(([category, count]) => (
                      <div
                        key={category}
                        className={`px-3 py-1 rounded-full text-sm font-medium ${ImageQualityService.getCategoryColor(category)}`}
                      >
                        {category}: {count}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Individual Results */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Individual Results</h4>
                <div className="space-y-3">
                  {analysisResult.results.map((result, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border ${
                        result.success 
                          ? 'bg-gray-50 border-gray-200' 
                          : 'bg-red-50 border-red-200'
                      }`}
                    >
                      <div className="flex items-center space-x-4">
                        <div className="w-16 h-16 rounded-lg overflow-hidden border border-gray-200 flex-shrink-0">
                          <img
                            src={URL.createObjectURL(files[index])}
                            alt={`Image ${index + 1}`}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <span className="font-medium text-gray-900">
                              Image {index + 1}
                            </span>
                            {result.success && getCategoryIcon(result.category)}
                          </div>
                          
                          {result.success ? (
                            <div className="flex items-center space-x-4 text-sm">
                              <span className="text-gray-600">
                                Score: <span className="font-medium">{result.qualityScore.toFixed(1)}</span>
                              </span>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${ImageQualityService.getCategoryColor(result.category)}`}>
                                {result.category}
                              </span>
                              <span className="text-gray-500">
                                {result.processingTime.toFixed(3)}s
                              </span>
                            </div>
                          ) : (
                            <p className="text-red-600 text-sm">
                              Error: {result.error}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default ImageQualityAnalyzer;
