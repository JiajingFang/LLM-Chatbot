export interface ChatRequest {
  prompt: string;
}

export interface ResponseContent {
    openai: string;
    anthropic: string;
}

export interface ChatResponse {
  response: ResponseContent;
}

export interface CompareResponse {
  claude_response: string;
  openai_response: string;
  summary: string;
  comparison: string;
  processing_time?: number;
}

export type Mode = 'chat' | 'compare';

export interface ApiError {
  message: string;
  status?: number;
}