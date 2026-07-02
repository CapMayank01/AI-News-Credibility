'use client';

import React, { useState } from 'react';

interface ResultCardProps {
  title: string;
  value: string | number;
  icon?: string;
  color?: 'success' | 'danger' | 'warning' | 'neutral';
}

const ResultCard: React.FC<ResultCardProps> = ({ title, value, icon, color = 'neutral' }) => {
  const colorClasses = {
    success: 'bg-green-50 border-green-200 text-green-900',
    danger: 'bg-red-50 border-red-200 text-red-900',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
    neutral: 'bg-blue-50 border-blue-200 text-blue-900',
  };

  return (
    <div className={`border rounded-lg p-6 ${colorClasses[color]}`}>
      <h3 className="text-sm font-semibold">{title}</h3>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
};

export default ResultCard;
