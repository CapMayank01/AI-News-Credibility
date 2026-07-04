"""
PHASE 11: FASTAPI BACKEND
Main API endpoints for news analysis.
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
import logging
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db, get_db
from app.models.database import Analysis, Base
from app.schemas.analysis import (
    AnalysisRequest, AnalysisResponse, AnalysisURLRequest,
    DashboardStats, AnalysisHistoryResponse, AnalysisHistory,
    HealthResponse, ComponentBreakdown, SimilarArticle
)
from app.services.analysis_service import AnalysisService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug
)

# Add CORS middleware
allow_origins = settings.cors_origins
allow_credentials = True
if "*" in allow_origins or not allow_origins:
    allow_origins = ["*"]
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
analysis_service: Optional[AnalysisService] = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    global analysis_service
    
    logger.info("=" * 50)
    logger.info("INITIALIZING APPLICATION")
    logger.info("=" * 50)
    
    # Initialize database
    init_db()
    
    # Initialize analysis service
    try:
        analysis_service = AnalysisService()
        logger.info("Analysis service initialized")
    except Exception as e:
        logger.error(f"Failed to initialize analysis service: {e}")
        raise


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_loaded": {
            "fake_news_model": analysis_service.fake_news_model is not None,
            "clickbait_model": analysis_service.clickbait_model is not None,
            "semantic_engine": analysis_service.semantic_engine is not None
        },
        "database_connected": True
    }


@app.post("/analyze-text", response_model=AnalysisResponse)
async def analyze_text(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze news article text.
    
    Args:
        request: Analysis request with article text
        db: Database session
        
    Returns:
        Detailed analysis results
    """
    try:
        if not analysis_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        result = analysis_service.analyze_text(
            text=request.text,
            headline=request.headline,
            source_url=request.source_url
        )
        
        # Save to database
        analysis_record = Analysis(
            headline=request.headline,
            content=request.text,
            source_url=request.source_url,
            prediction=0 if result['prediction'] == 'Fake' else 1,
            model_confidence=result['model_confidence'],
            source_score=result['source_score'],
            clickbait_score=result['clickbait_score'],
            reliability_score=result['reliability_score']
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
        
        result['analysis_id'] = analysis_record.id
        result['created_at'] = analysis_record.created_at
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-url", response_model=AnalysisResponse)
async def analyze_url(
    request: AnalysisURLRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze news article from URL.
    
    Args:
        request: Analysis request with URL
        db: Database session
        
    Returns:
        Detailed analysis results
    """
    try:
        if not analysis_service:
            raise HTTPException(status_code=500, detail="Service not initialized")
        
        # Fetch content from URL
        content = analysis_service.fetch_url_content(str(request.url))
        
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract content from URL")
        
        # Analyze
        result = analysis_service.analyze_text(
            text=content.get('content', ''),
            headline=content.get('headline'),
            source_url=str(request.url)
        )
        
        # Save to database
        analysis_record = Analysis(
            headline=content.get('headline'),
            content=content.get('content', ''),
            source_url=str(request.url),
            prediction=0 if result['prediction'] == 'Fake' else 1,
            model_confidence=result['model_confidence'],
            source_score=result['source_score'],
            clickbait_score=result['clickbait_score'],
            reliability_score=result['reliability_score']
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
        
        result['analysis_id'] = analysis_record.id
        result['created_at'] = analysis_record.created_at
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=AnalysisHistoryResponse)
async def get_history(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get analysis history.
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        db: Database session
        
    Returns:
        Paginated analysis history
    """
    try:
        # Get total count
        total = db.query(Analysis).count()
        
        # Get paginated results
        skip = (page - 1) * page_size
        analyses = db.query(Analysis).offset(skip).limit(page_size).all()
        
        items = [
            AnalysisHistory(
                analysis_id=analysis.id,
                prediction='Real' if analysis.prediction == 1 else 'Fake',
                reliability_score=analysis.reliability_score,
                source_score=analysis.source_score,
                headline=analysis.headline,
                created_at=analysis.created_at
            )
            for analysis in analyses
        ]
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard-stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics.
    
    Args:
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    try:
        analyses = db.query(Analysis).all()
        
        if not analyses:
            return {
                "total_analyses": 0,
                "fake_percentage": 0,
                "real_percentage": 0,
                "average_confidence": 0,
                "average_reliability": 0
            }
        
        total = len(analyses)
        fake_count = sum(1 for a in analyses if a.prediction == 0)
        real_count = total - fake_count
        
        return {
            "total_analyses": total,
            "fake_percentage": (fake_count / total * 100) if total > 0 else 0,
            "real_percentage": (real_count / total * 100) if total > 0 else 0,
            "average_confidence": sum(a.model_confidence for a in analyses) / total,
            "average_reliability": sum(a.reliability_score for a in analyses) / total
        }
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
