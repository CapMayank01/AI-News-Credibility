"""
PHASE 12: DATABASE DESIGN
SQLAlchemy models for news analyses and trusted sources.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Analysis(Base):
    """
    Stores news analysis results.
    """
    __tablename__ = 'analyses'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    headline = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    source_url = Column(String(500), nullable=True)
    
    # Predictions
    prediction = Column(Integer, nullable=False)  # 0=Fake, 1=Real
    model_confidence = Column(Float, nullable=False)  # 0-1
    
    # Scores
    source_score = Column(Float, nullable=False)  # 0-100
    clickbait_score = Column(Float, nullable=False)  # 0-1
    reliability_score = Column(Float, nullable=False)  # 0-100
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrustedSource(Base):
    """
    Stores trusted news sources and their credibility scores.
    """
    __tablename__ = 'trusted_sources'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(String(255), unique=True, nullable=False)
    credibility_score = Column(Float, nullable=False)  # 0-100
    description = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AnalysisHistory(Base):
    """
    Extended analysis history with additional metadata.
    """
    __tablename__ = 'analysis_history'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, nullable=False)
    
    # Keywords extracted
    top_keywords = Column(String(500), nullable=True)
    
    # Similar articles count
    similar_articles_count = Column(Integer, default=0)
    similar_articles_avg_score = Column(Float, nullable=True)
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    is_correct = Column(Boolean, nullable=True)  # User validation
    
    created_at = Column(DateTime, default=datetime.utcnow)
