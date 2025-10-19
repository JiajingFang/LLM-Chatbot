import axios, { AxiosError } from 'axios';
import type { ChatRequest, ChatResponse, CompareResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    config.headers['x-api-token'] = 'user2_token';
    console.log(`📤 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('❌ API Error:', error.message);
    return Promise.reject(error);
  }
);

export const chatApi = async (data: ChatRequest): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>('/chat', data);
  return response.data;
};

export const compareApi = async (data: ChatRequest): Promise<CompareResponse> => {
  const response = await apiClient.post<CompareResponse>('/compare', data);
  return response.data;
};

export { apiClient };