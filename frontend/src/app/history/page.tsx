'use client';

import React, { useState, useEffect } from 'react';
import { analysisService } from '@/services/api';

export default function HistoryPage() {
  const [history, setHistory] = useState<any>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      setError(null);
      try {
        const historyData = await analysisService.getHistory(page, pageSize);
        setHistory(historyData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load history');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [page, pageSize]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-900 rounded-lg p-4">
        ❌ {error}
      </div>
    );
  }

  const getPredictionBadge = (prediction: string) => {
    return prediction === 'Real'
      ? 'bg-green-100 text-green-800'
      : 'bg-red-100 text-red-800';
  };

  const getReliabilityColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold mb-2">Analysis History</h1>
        <p className="text-gray-600">View all previous news credibility analyses</p>
      </div>

      {/* Table */}
      {history && history.items && history.items.length > 0 ? (
        <>
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Headline</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Prediction</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Reliability</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Source Score</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {history.items.map((item: any, index: number) => (
                    <tr key={index} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {new Date(item.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 font-medium">
                        {item.headline || 'N/A'}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getPredictionBadge(item.prediction)}`}>
                          {item.prediction}
                        </span>
                      </td>
                      <td className={`px-6 py-4 text-sm font-bold ${getReliabilityColor(item.reliability_score)}`}>
                        {item.reliability_score.toFixed(1)}/100
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {item.source_score.toFixed(0)}/100
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Pagination */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              Showing {(page - 1) * pageSize + 1}-{Math.min(page * pageSize, history.total)} of {history.total} analyses
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
              >
                ← Previous
              </button>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Page {page}</span>
              </div>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page * pageSize >= history.total}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
              >
                Next →
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-blue-50 border border-blue-200 text-blue-900 rounded-lg p-8 text-center">
          <div className="text-4xl mb-4">📭</div>
          <p className="text-lg font-semibold">No analyses yet</p>
          <p className="text-sm mt-2">Start analyzing news articles to see them here</p>
        </div>
      )}
    </div>
  );
}
