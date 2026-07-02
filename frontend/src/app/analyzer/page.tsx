'use client';

import React, { useState } from 'react';
import { analysisService } from '@/services/api';
import AnalysisResults from '@/components/AnalysisResults';
import { AnalysisResult } from '@/types';

export default function AnalyzerPage() {
  const [text, setText] = useState('');
  const [headline, setHeadline] = useState('');
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState<'text' | 'url'>('text');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter article text');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const analysisResult = await analysisService.analyzeText(text, headline);
      setResult(analysisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeUrl = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const analysisResult = await analysisService.analyzeUrl(url);
      setResult(analysisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">News Analyzer</h1>
        <p className="text-gray-600">Enter news article text or URL to analyze credibility</p>
      </div>

      {!result ? (
        <>
          {/* Mode Selection */}
          <div className="flex gap-4 justify-center mb-8">
            <button
              onClick={() => setMode('text')}
              className={`px-6 py-2 rounded-lg font-bold transition ${
                mode === 'text'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
            >
              📝 Analyze Text
            </button>
            <button
              onClick={() => setMode('url')}
              className={`px-6 py-2 rounded-lg font-bold transition ${
                mode === 'url'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
            >
              🔗 Analyze URL
            </button>
          </div>

          {/* Input Section */}
          <div className="bg-white border border-gray-200 rounded-lg p-8 space-y-6">
            {mode === 'text' ? (
              <>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Headline (Optional)
                  </label>
                  <input
                    type="text"
                    value={headline}
                    onChange={(e) => setHeadline(e.target.value)}
                    placeholder="Enter article headline..."
                    className="input"
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Article Text *
                  </label>
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste article content here..."
                    className="input h-64 resize-none"
                  />
                </div>
                <button
                  onClick={handleAnalyzeText}
                  disabled={loading}
                  className="btn btn-primary w-full py-3 text-lg disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze Text'}
                </button>
              </>
            ) : (
              <>
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Article URL *
                  </label>
                  <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com/article"
                    className="input"
                  />
                </div>
                <button
                  onClick={handleAnalyzeUrl}
                  disabled={loading}
                  className="btn btn-primary w-full py-3 text-lg disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze URL'}
                </button>
              </>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-900 rounded-lg p-4">
              ❌ {error}
            </div>
          )}
        </>
      ) : (
        <>
          {/* Results */}
          <AnalysisResults result={result} />

          {/* New Analysis Button */}
          <div className="text-center">
            <button
              onClick={() => {
                setResult(null);
                setText('');
                setHeadline('');
                setUrl('');
              }}
              className="btn btn-primary"
            >
              Analyze Another Article
            </button>
          </div>
        </>
      )}
    </div>
  );
}
