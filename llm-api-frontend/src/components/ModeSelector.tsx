import React from 'react';
import type { Mode } from '../types';

interface ModeSelectorProps {
  currentMode: Mode;
  onModeChange: (mode: Mode) => void;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({ currentMode, onModeChange }) => {
  return (
    <div className="flex justify-center gap-4 mb-8">
      <button
        onClick={() => onModeChange('chat')}
        className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
          currentMode === 'chat'
            ? 'bg-white text-purple-600 shadow-lg'
            : 'bg-white/20 text-white hover:bg-white/30'
        }`}
      >
        💬 双模型对话
      </button>
      <button
        onClick={() => onModeChange('compare')}
        className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
          currentMode === 'compare'
            ? 'bg-white text-purple-600 shadow-lg'
            : 'bg-white/20 text-white hover:bg-white/30'
        }`}
      >
        🔍 深度对比分析
      </button>
    </div>
  );
};
