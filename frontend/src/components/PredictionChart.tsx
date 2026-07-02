'use client';

import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

interface PredictionChartProps {
  fakePercentage: number;
  realPercentage: number;
}

const PredictionChart: React.FC<PredictionChartProps> = ({ fakePercentage, realPercentage }) => {
  const data = [
    { name: 'Fake News', value: fakePercentage },
    { name: 'Real News', value: realPercentage },
  ];

  const COLORS = ['#ff6b6b', '#4ecdc4'];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name}: ${value.toFixed(1)}%`} outerRadius={80} fill="#8884d8" dataKey="value">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => `${Number(value).toFixed(1)}%`} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default PredictionChart;
