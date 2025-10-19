import React, { useState } from 'react';
import type { KeyboardEvent } from 'react';

interface InputSectionProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
}

export const InputSection: React.FC<InputSectionProps> = ({ onSubmit, isLoading }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = () => {
    if (question.trim()) {
      onSubmit(question);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.ctrlKey && e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="mb-8">
      <div className="flex gap-4 items-start">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="please enter your question here...&#10;e.g. Please explain what is Bitcoin？&#10;&#10;hint：please Ctrl+Enter to submit"
          className="flex-1 p-4 border-2 border-gray-200 rounded-xl resize-vertical min-h-[120px] focus:outline-none focus:border-purple-500 transition-colors"
          disabled={isLoading}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !question.trim()}
          className="px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-800 text-white rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5"
        >
          {isLoading ? 'Loading...' : 'Send'}
        </button>
      </div>
    </div>
  );
};