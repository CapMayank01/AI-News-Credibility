"""
Configuration settings.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    api_title: str = "AI-Powered News Credibility Assessment"
    api_version: str = "1.0.0"
    debug: bool = os.getenv('DEBUG', 'False') == 'True'

    @field_validator('debug', mode='before')
    @classmethod
    def parse_debug(cls, value):
        """Treat common development values as true and everything else as false."""
        if isinstance(value, str):
            return value.strip().lower() in {'1', 'true', 'yes', 'on', 'debug', 'development'}
        return bool(value)
    
    # Database
    database_url: str = os.getenv(
        'DATABASE_URL',
        'sqlite:///./news_credibility.db'
    )

    @field_validator('database_url', mode='before')
    @classmethod
    def parse_database_url(cls, value):
        """Fix postgres:// to postgresql:// for SQLAlchemy."""
        if isinstance(value, str) and value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql://", 1)
        return value
    
    # Models
    model_path: str = os.getenv(
        'MODEL_PATH',
        './ml_models/distilbert_model_best.pt'
    )
    tokenizer_path: str = os.getenv(
        'TOKENIZER_PATH', './ml_models/distilbert_tokenizer'
    )
    clickbait_model_path: str = os.getenv(
        'CLICKBAIT_MODEL_PATH',
        './ml_models/clickbait_model.joblib'
    )
    clickbait_vectorizer_path: str = os.getenv(
        'CLICKBAIT_VECTORIZER_PATH', './ml_models/clickbait_tfidf.joblib'
    )
    faiss_index_path: str = os.getenv(
        'FAISS_INDEX_PATH',
        './faiss_index/trusted_articles_index.faiss'
    )
    faiss_articles_path: str = os.getenv(
        'FAISS_ARTICLES_PATH', './faiss_index/trusted_articles.pkl'
    )
    embedder_model: str = os.getenv(
        'EMBEDDER_MODEL',
        'all-MiniLM-L6-v2'
    )
    source_credibility_path: str = os.getenv(
        'SOURCE_CREDIBILITY_PATH',
        './backend/app/data/source_credibility.json'
    )
    
    # ML Configuration
    max_sequence_length: int = 512
    batch_size: int = 32
    device: str = os.getenv('DEVICE', 'cpu')
    
    # CORS
    cors_origins: Any = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000"
    ]

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, value):
        """Parse CORS origins if passed as string or JSON list."""
        if isinstance(value, str):
            value = value.strip()
            if value.startswith('[') and value.endswith(']'):
                import json
                try:
                    return json.loads(value)
                except Exception:
                    pass
            if ',' in value:
                return [orig.strip() for orig in value.split(',')]
            return [value]
        return value
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600  # 1 hour
    
    class Config:
        env_file = '.env'
        protected_namespaces = ()


settings = Settings()
