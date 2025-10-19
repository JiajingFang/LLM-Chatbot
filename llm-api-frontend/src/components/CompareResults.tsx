import React from 'react';
import type { CompareResponse } from '../types';
import { ResponseCard } from './ResponseCard';

interface CompareResultsProps {
  data: CompareResponse;
  processingTime?: number;
}

export const CompareResults: React.FC<CompareResultsProps> = ({ data, processingTime }) => {
  return (
    <div className="space-y-6">
      {/* Original Responses */}
      <div className="grid md:grid-cols-2 gap-6">
        <ResponseCard model="claude" content={data.claude_response} />
        <ResponseCard model="openai" content={data.openai_response} />
      </div>

      {/* Summary Section */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border-2 border-purple-200">
        <div className="flex items-center gap-3 mb-4">
          <span className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center">
            📝
          </span>
          <h3 className="text-xl font-bold text-purple-800">Summary</h3>
        </div>
        <div className="bg-white rounded-xl p-5 text-gray-800 leading-relaxed whitespace-pre-wrap">
          {data.summary}
        </div>
      </div>

      {/* Comparison Section */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border-2 border-purple-200">
        <div className="flex items-center gap-3 mb-4">
          <span className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center">
            ⚖️
          </span>
          <h3 className="text-xl font-bold text-purple-800">Comparison</h3>
        </div>
        <div className="bg-white rounded-xl p-5 text-gray-800 leading-relaxed whitespace-pre-wrap">
          {data.comparison}
        </div>
      </div>

      {processingTime && (
        <div className="text-center text-gray-600 text-sm">
          ⏱️ ProcessingTime: {processingTime.toFixed(2)} 秒
        </div>
      )}
    </div>
  );
};