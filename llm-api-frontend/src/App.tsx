import { useState } from 'react';
import type { Mode, ChatResponse, CompareResponse } from './types';
import { chatApi, compareApi } from './services/api';
import { ModeSelector } from './components/ModeSelector';
import { InputSection } from './components/InputSection';
import { Loading } from './components/Loading';
import { ChatResults } from './components/ChatResults';
import { CompareResults } from './components/CompareResults';
import { ErrorMessage } from './components/ErrorMessage';

function App() {
  const [mode, setMode] = useState<Mode>('chat');
  const [isLoading, setIsLoading] = useState(false);
  const [chatData, setChatData] = useState<ChatResponse | null>(null);
  const [compareData, setCompareData] = useState<CompareResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processingTime, setProcessingTime] = useState<number | null>(null);

  const handleModeChange = (newMode: Mode) => {
    setMode(newMode);
    setChatData(null);
    setCompareData(null);
    setError(null);
  };

  const handleSubmit = async (question: string) => {
    setIsLoading(true);
    setError(null);
    setChatData(null);
    setCompareData(null);
    
    const startTime = Date.now();

    try {
      if (mode === 'chat') {
        const data = await chatApi({ prompt: question });
        setChatData(data);
      } else {
        const data = await compareApi({ prompt: question });
        setCompareData(data);
      }
      
      const endTime = Date.now();
      setProcessingTime((endTime - startTime) / 1000);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || '请求失败，请稍后重试';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-purple-900 p-5">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center text-white mb-10">
          <h1 className="text-5xl font-bold mb-3 drop-shadow-lg">
            🤖 LLM 智能对比平台
          </h1>
          <p className="text-xl opacity-90">
            同时对比 Claude 和 OpenAI 的回答质量
          </p>
        </header>

        {/* Mode Selector */}
        <ModeSelector currentMode={mode} onModeChange={handleModeChange} />

        {/* Main Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8">
          {/* Input Section */}
          <InputSection onSubmit={handleSubmit} isLoading={isLoading} />

          {/* Loading */}
          {isLoading && <Loading />}

          {/* Error */}
          {error && <ErrorMessage message={error} />}

          {/* Results */}
          {!isLoading && !error && mode === 'chat' && chatData && (
            <ChatResults data={chatData} processingTime={processingTime || undefined} />
          )}

          {!isLoading && !error && mode === 'compare' && compareData && (
            <CompareResults data={compareData} processingTime={processingTime || undefined} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;