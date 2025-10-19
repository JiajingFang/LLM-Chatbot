import React from 'react';
import type { ChatResponse } from '../types';
import { ResponseCard } from './ResponseCard';

interface ChatResultsProps {
  data: ChatResponse;
  processingTime?: number;
}

export const ChatResults: React.FC<ChatResultsProps> = ({ data, processingTime }) => {
  return (
    <div>
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <ResponseCard model="claude" content={data.response.anthropic} />
        <ResponseCard model="openai" content={data.response.openai} />
      </div>
      {processingTime && (
        <div className="text-center text-gray-600 text-sm">
          ⏱️ ProcessingTime: {processingTime.toFixed(2)} 秒
        </div>
      )}
    </div>
  );
};