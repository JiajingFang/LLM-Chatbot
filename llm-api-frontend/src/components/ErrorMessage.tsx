import React from 'react';

interface ErrorMessageProps {
  message: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return (
    <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl">
      <p className="font-semibold">❌ Error</p>
      <p className="mt-1">{message}</p>
    </div>
  );
};
