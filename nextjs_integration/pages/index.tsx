import React from 'react';
import Head from 'next/head';
import ImageQualityAnalyzer from '../components/ImageQualityAnalyzer';
import { BatchAnalysisResult } from '../lib/imageQualityService';

export default function Home() {
  const handleAnalysisComplete = (result: BatchAnalysisResult) => {
    console.log('Analysis completed:', result);
    
    // You can add additional logic here, such as:
    // - Save results to database
    // - Send analytics data
    // - Show notifications
    // - Update parent component state
  };

  return (
    <>
      <Head>
        <title>Image Quality Analyzer - Next.js</title>
        <meta name="description" content="Analyze image quality using advanced IL-NIQE algorithm" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gray-50">
        <ImageQualityAnalyzer onAnalysisComplete={handleAnalysisComplete} />
      </main>
    </>
  );
}
