import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface AnalysisResponse {
  analysis_id: string;
  prediction: string;
  model_confidence: number;
  reliability_score: number;
  classification: string;
  source_score: number;
  clickbait_score: number;
  similar_articles: Array<{
    title: string;
    source: string;
    similarity_score: number;
  }>;
  explanation: any;
  recommendation: string;
  component_breakdown: {
    model_confidence: number;
    source_credibility: number;
    similarity_score: number;
    clickbait_score: number;
  };
  created_at: string;
}

interface DashboardStats {
  total_analyses: number;
  fake_percentage: number;
  real_percentage: number;
  average_confidence: number;
  average_reliability: number;
}

interface AnalysisHistory {
  total: number;
  page: number;
  page_size: number;
  items: Array<{
    analysis_id: string;
    prediction: string;
    reliability_score: number;
    source_score: number;
    headline: string | null;
    created_at: string;
  }>;
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analysisService = {
  analyzeText: async (text: string, headline?: string, sourceUrl?: string): Promise<AnalysisResponse> => {
    const response = await apiClient.post('/analyze-text', {
      text,
      headline,
      source_url: sourceUrl,
    });
    return response.data;
  },

  analyzeUrl: async (url: string): Promise<AnalysisResponse> => {
    const response = await apiClient.post('/analyze-url', {
      url,
      extract_content: true,
    });
    return response.data;
  },

  getHistory: async (page: number = 1, pageSize: number = 10): Promise<AnalysisHistory> => {
    const response = await apiClient.get('/history', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await apiClient.get('/dashboard-stats');
    return response.data;
  },

  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
