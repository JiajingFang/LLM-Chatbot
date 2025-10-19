import React from 'react';

interface ResponseCardProps {
  model: 'claude' | 'openai';
  content: string;
}

export const ResponseCard: React.FC<ResponseCardProps> = ({ model, content }) => {
  const config = {
    claude: {
      name: 'Claude',
      color: 'orange',
      icon: 'C',
      bgColor: 'bg-orange-50',
      borderColor: 'border-l-orange-500',
      badgeBg: 'bg-orange-500',
    },
    openai: {
      name: 'OpenAI',
      color: 'green',
      icon: 'O',
      bgColor: 'bg-green-50',
      borderColor: 'border-l-green-500',
      badgeBg: 'bg-green-500',
    },
  };

  const { name, icon, bgColor, borderColor, badgeBg } = config[model];

  return (
    <div className={`${bgColor} rounded-2xl p-6 border-l-4 ${borderColor}`}>
      <div className="flex items-center gap-2 mb-4">
        <span className={`${badgeBg} text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center gap-2`}>
          <span className="w-6 h-6 bg-white rounded-full flex items-center justify-center text-xs font-bold" style={{ color: config[model].color }}>
            {icon}
          </span>
          {name}
        </span>
      </div>
      <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
        {content}
      </div>
    </div>
  );
};