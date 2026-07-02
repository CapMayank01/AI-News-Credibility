"""
PHASE 11: FASTAPI SCHEMAS
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime


class AnalysisRequest(BaseModel):
    """Request body for text analysis."""
    text: str = Field(..., min_length=10, max_length=10000)
    headline: Optional[str] = None
    source_url: Optional[str] = None


class AnalysisURLRequest(BaseModel):
    """Request body for URL analysis."""
    url: HttpUrl
    extract_content: bool = True


class SimilarArticle(BaseModel):
    """Similar article in results."""
    title: str
    source: str
    similarity_score: float
    url: Optional[str] = None


class ComponentBreakdown(BaseModel):
    """Breakdown of reliability score components."""
    model_confidence: float
    source_credibility: float
    similarity_score: float
    clickbait_score: float


class AnalysisResponse(BaseModel):
    """Response for analysis request."""
    analysis_id: str
    prediction: str  # "Real" or "Fake"
    model_confidence: float
    reliability_score: float
    classification: str  # "Highly Reliable", "Reliable", etc.
    source_score: float
    clickbait_score: float
    similar_articles: List[SimilarArticle]
    explanation: Dict
    recommendation: str
    component_breakdown: ComponentBreakdown
    created_at: datetime


class DashboardStats(BaseModel):
    """Dashboard statistics."""
    total_analyses: int
    fake_percentage: float
    real_percentage: float
    average_confidence: float
    average_reliability: float


class AnalysisHistory(BaseModel):
    """Historical analysis entry."""
    analysis_id: str
    prediction: str
    reliability_score: float
    source_score: float
    headline: Optional[str]
    created_at: datetime


class AnalysisHistoryResponse(BaseModel):
    """Paginated history response."""
    total: int
    page: int
    page_size: int
    items: List[AnalysisHistory]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    models_loaded: Dict[str, bool]
    database_connected: bool
