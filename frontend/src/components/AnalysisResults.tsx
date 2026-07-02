'use client';

import React from 'react';
import { AnalysisResult } from '@/types';
import ResultCard from './ResultCard';

interface AnalysisResultsProps {
  result: AnalysisResult;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result }) => {
  const getPredictionColor = (): 'success' | 'danger' => {
    return result.prediction === 'Real' ? 'success' : 'danger';
  };

  const getClassificationColor = () => {
    if (result.classification === 'Highly Reliable') return 'success';
    if (result.classification === 'Reliable') return 'neutral';
    if (result.classification === 'Questionable') return 'warning';
    return 'danger';
  };

  return (
    <div className="space-y-8">
      {/* Main Results */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ResultCard
          title="Prediction"
          value={result.prediction}
          color={getPredictionColor()}
        />
        <ResultCard
          title="Reliability Score"
          value={`${result.reliability_score.toFixed(1)}/100`}
          color={getClassificationColor()}
        />
        <ResultCard
          title="Model Confidence"
          value={`${(result.model_confidence * 100).toFixed(1)}%`}
        />
      </div>

      {/* Classification */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-2">Classification</h3>
        <p className="text-lg text-gray-700 mb-4">{result.classification}</p>
        <p className="text-gray-600 italic">{result.recommendation}</p>
      </div>

      {/* Scores Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-blue-900">Source Credibility</p>
          <p className="text-2xl font-bold text-blue-900">{result.source_score.toFixed(0)}</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-purple-900">Clickbait Score</p>
          <p className="text-2xl font-bold text-purple-900">{(result.clickbait_score * 100).toFixed(1)}%</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-green-900">Model Confidence</p>
          <p className="text-2xl font-bold text-green-900">{(result.component_breakdown.model_confidence).toFixed(1)}%</p>
        </div>
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <p className="text-sm font-semibold text-orange-900">Similarity Score</p>
          <p className="text-2xl font-bold text-orange-900">{(result.component_breakdown.similarity_score).toFixed(1)}%</p>
        </div>
      </div>

      {/* Similar Articles */}
      {result.similar_articles && result.similar_articles.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Similar Trusted Articles</h3>
          <div className="space-y-3">
            {result.similar_articles.map((article, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                <p className="font-semibold">{article.title}</p>
                <div className="flex justify-between items-center mt-1">
                  <span className="text-sm text-gray-600">{article.source}</span>
                  <span className="text-sm font-bold text-blue-600">
                    {article.similarity_score.toFixed(1)}% match
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Explanation */}
      {result.explanation && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Analysis Explanation</h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-700">Summary</h4>
              <p className="text-gray-600">{result.explanation.summary}</p>
            </div>
            {result.explanation.source_analysis && (
              <div>
                <h4 className="font-semibold text-gray-700">Source Analysis</h4>
                <p className="text-gray-600">{result.explanation.source_analysis.explanation}</p>
              </div>
            )}
            {result.explanation.clickbait_analysis && (
              <div>
                <h4 className="font-semibold text-gray-700">Clickbait Analysis</h4>
                <p className="text-gray-600">{result.explanation.clickbait_analysis.explanation}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
