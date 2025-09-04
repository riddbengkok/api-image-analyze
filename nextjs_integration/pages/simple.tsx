import React from 'react';
import Head from 'next/head';
import SimpleImageAnalyzer from '../components/SimpleImageAnalyzer';

export default function SimplePage() {
  return (
    <>
      <Head>
        <title>Simple Image Quality Analyzer</title>
        <meta name="description" content="Simple image quality analysis tool" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gray-100 py-8">
        <SimpleImageAnalyzer />
      </main>
    </>
  );
}
