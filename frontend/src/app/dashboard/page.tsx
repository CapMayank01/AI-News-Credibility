'use client';

import React, { useState, useEffect } from 'react';
import { analysisService } from '@/services/api';
import PredictionChart from '@/components/PredictionChart';
import ResultCard from '@/components/ResultCard';
import { DashboardStats } from '@/types';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const dashboardStats = await analysisService.getDashboardStats();
        setStats(dashboardStats);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-900 rounded-lg p-4">
        ❌ {error || 'Failed to load dashboard'}
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-600">Real-time analytics of news credibility analyses</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <ResultCard
          title="Total Analyses"
          value={stats.total_analyses}
        />
        <ResultCard
          title="Average Confidence"
          value={`${stats.average_confidence.toFixed(1)}%`}
        />
        <ResultCard
          title="Average Reliability"
          value={`${stats.average_reliability.toFixed(1)}`}
        />
        <ResultCard
          title="Analysis Rate"
          value={`${((stats.total_analyses / Math.max(stats.total_analyses, 1)) * 100).toFixed(0)}%`}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Prediction Distribution */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Prediction Distribution</h2>
          <PredictionChart
            fakePercentage={stats.fake_percentage}
            realPercentage={stats.real_percentage}
          />
        </div>

        {/* Statistics Summary */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-bold mb-4">Summary Statistics</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-700">Total Articles Analyzed</span>
              <span className="font-bold">{stats.total_analyses}</span>
            </div>
            <div className="border-t border-gray-200 pt-3">
              <div className="flex justify-between mb-2">
                <span className="text-gray-700">Fake News Detected</span>
                <span className="font-bold text-red-600">{stats.fake_percentage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded h-2">
                <div
                  className="bg-red-600 rounded h-2 transition-all"
                  style={{ width: `${stats.fake_percentage}%` }}
                />
              </div>
            </div>
            <div className="flex justify-between mb-2">
              <span className="text-gray-700">Real News Identified</span>
              <span className="font-bold text-green-600">{stats.real_percentage.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded h-2">
              <div
                className="bg-green-600 rounded h-2 transition-all"
                style={{ width: `${stats.real_percentage}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Additional Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-blue-900 mb-2">Average Model Confidence</h3>
          <p className="text-3xl font-bold text-blue-600">{(stats.average_confidence * 100).toFixed(1)}%</p>
          <p className="text-sm text-blue-700 mt-2">Overall prediction confidence across all analyses</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-purple-900 mb-2">Average Reliability Score</h3>
          <p className="text-3xl font-bold text-purple-600">{stats.average_reliability.toFixed(1)}/100</p>
          <p className="text-sm text-purple-700 mt-2">Composite reliability across all articles</p>
        </div>
      </div>
    </div>
  );
}
