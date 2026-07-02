export interface AnalysisResult {
  analysis_id: string;
  prediction: string;
  model_confidence: number;
  reliability_score: number;
  classification: string;
  source_score: number;
  clickbait_score: number;
  similar_articles: SimilarArticle[];
  explanation: ExplanationData;
  recommendation: string;
  component_breakdown: ComponentBreakdown;
  created_at: string;
}

export interface SimilarArticle {
  title: string;
  source: string;
  similarity_score: number;
  url?: string;
}

export interface ExplanationData {
  summary: string;
  model_explanation: any;
  source_analysis: SourceAnalysis;
  clickbait_analysis: ClickbaitAnalysis;
  similarity_analysis: SimilarityAnalysis;
  overall_assessment: string;
}

export interface SourceAnalysis {
  score: number;
  explanation: string;
}

export interface ClickbaitAnalysis {
  probability: number;
  explanation: string;
}

export interface SimilarityAnalysis {
  similar_articles_found: number;
  average_similarity: number;
  explanation: string;
  top_matches?: SimilarArticle[];
}

export interface ComponentBreakdown {
  model_confidence: number;
  source_credibility: number;
  similarity_score: number;
  clickbait_score: number;
}

export interface DashboardStats {
  total_analyses: number;
  fake_percentage: number;
  real_percentage: number;
  average_confidence: number;
  average_reliability: number;
}
