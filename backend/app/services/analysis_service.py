"""
Analysis Service
Orchestrates all ML models and analysis pipelines.
"""

import logging
from typing import Dict, Optional, List
import requests
from bs4 import BeautifulSoup
import numpy as np

from app.core.config import settings
from app.utils.text_cleaner import TextCleaner
from app.utils.source_credibility import SourceCredibilityEngine
from app.utils.semantic_similarity import SemanticSimilarityEngine
from app.utils.reliability_scorer import ReliabilityScorer
from app.utils.explainability import ExplainabilityModule
from app.utils.clickbait_detector import ClickbaitDetector
from app.utils.distilbert_model import DistilBertTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Main service that orchestrates all analysis components.
    """
    
    def __init__(self):
        """Initialize all models and engines."""
        logger.info("Initializing AnalysisService...")
        
        try:
            # Initialize text cleaner
            self.text_cleaner = TextCleaner()
            logger.info("Text cleaner initialized")
            
            # Initialize source credibility engine
            self.source_credibility_engine = SourceCredibilityEngine(
                settings.source_credibility_path
            )
            logger.info("Source credibility engine initialized")
            
            # Initialize semantic similarity engine (optional - loads if index exists)
            try:
                self.semantic_engine = SemanticSimilarityEngine(
                    model_name=settings.embedder_model,
                    device=settings.device
                )
                try:
                    self.semantic_engine.load_index(
                        settings.faiss_index_path, settings.faiss_articles_path
                    )
                    logger.info("Semantic similarity engine loaded with FAISS index")
                except:
                    logger.warning("FAISS index not found - semantic search unavailable")
                    self.semantic_engine = None
            except Exception as e:
                logger.warning(f"Could not initialize semantic engine: {e}")
                self.semantic_engine = None
            
            # Initialize fake news model
            try:
                self.fake_news_model = DistilBertTrainer(
                    device=settings.device,
                    tokenizer_path=settings.tokenizer_path,
                    pretrained=False
                )
                self.fake_news_model.load(settings.model_path)
                logger.info("Fake news DistilBERT model loaded")
            except Exception as e:
                logger.warning(f"Could not load DistilBERT model: {e}")
                self.fake_news_model = None
            
            # Initialize clickbait detector
            try:
                self.clickbait_model = ClickbaitDetector()
                self.clickbait_model.load(
                    settings.clickbait_model_path,
                    settings.clickbait_vectorizer_path
                )
                logger.info("Clickbait detection model loaded")
            except Exception as e:
                logger.warning(f"Could not load clickbait model: {e}")
                self.clickbait_model = None
            
            logger.info("AnalysisService initialization complete")
            
        except Exception as e:
            logger.error(f"Critical error initializing AnalysisService: {e}")
            raise
    
    def analyze_text(
        self,
        text: str,
        headline: Optional[str] = None,
        source_url: Optional[str] = None
    ) -> Dict:
        """
        Perform complete analysis on news text.
        
        Args:
            text: Article content
            headline: Article headline
            source_url: Article URL
            
        Returns:
            Complete analysis results
        """
        logger.info(f"Analyzing text: {headline or text[:50]}...")
        
        # Clean text
        cleaned_text = self.text_cleaner.clean_pipeline(text)
        
        # Get model prediction
        prediction, model_confidence = self._get_model_prediction(cleaned_text)
        
        # Get source credibility
        source_score = self._get_source_credibility(source_url)
        
        # Get clickbait score
        clickbait_score = self._get_clickbait_score(headline or text)
        
        # Get semantic similarity
        similarity_results = self._get_semantic_similarity(cleaned_text)
        
        # Calculate average similarity
        avg_similarity = self._calculate_avg_similarity(similarity_results)
        
        # Calculate reliability score
        reliability_data = ReliabilityScorer.calculate_score(
            model_confidence=model_confidence * 100,
            source_credibility=source_score,
            average_similarity=avg_similarity,
            clickbait_probability=clickbait_score
        )
        
        # Generate explanation
        explanation = ExplainabilityModule.generate_detailed_explanation(
            text=cleaned_text,
            model_prediction=prediction,
            model_confidence=model_confidence,
            source_score=source_score,
            clickbait_score=clickbait_score,
            similarity_results=similarity_results
        )
        
        # Build response
        return {
            'prediction': 'Real' if prediction == 1 else 'Fake',
            'model_confidence': float(model_confidence),
            'reliability_score': reliability_data['reliability_score'],
            'classification': reliability_data['classification'],
            'source_score': float(source_score),
            'clickbait_score': float(clickbait_score),
            'similar_articles': similarity_results[:5],
            'explanation': explanation,
            'recommendation': ReliabilityScorer.get_recommendation(
                reliability_data['reliability_score']
            ),
            'component_breakdown': {
                'model_confidence': float(model_confidence * 100),
                'source_credibility': float(source_score),
                'similarity_score': float(avg_similarity),
                'clickbait_score': float(clickbait_score)
            }
        }
    
    def _get_model_prediction(self, text: str) -> tuple:
        """Get prediction from fake news model."""
        if not self.fake_news_model:
            logger.warning("Model not available, returning default prediction")
            return 1, 0.5  # Default to real with low confidence
        
        try:
            predictions, probabilities = self.fake_news_model.predict([text])
            prediction = int(predictions[0])
            confidence = float(probabilities[0][prediction])
            return prediction, confidence
        except Exception as e:
            logger.error(f"Error getting model prediction: {e}")
            return 1, 0.5
    
    def _get_source_credibility(self, source_url: Optional[str]) -> float:
        """Get source credibility score."""
        if not source_url:
            return 50.0  # Default for unknown
        
        try:
            result = self.source_credibility_engine.get_credibility_score(source_url)
            return float(result['credibility_score'])
        except Exception as e:
            logger.error(f"Error getting source credibility: {e}")
            return 50.0
    
    def _get_clickbait_score(self, text: str) -> float:
        """Get clickbait probability."""
        if not self.clickbait_model:
            logger.warning("Clickbait model not available")
            return 0.0
        
        try:
            score = self.clickbait_model.predict_proba(np.array([text]))[0]
            return float(score)
        except Exception as e:
            logger.error(f"Error getting clickbait score: {e}")
            return 0.0
    
    def _get_semantic_similarity(self, text: str) -> List[Dict]:
        """Get similar articles from trusted sources."""
        if not self.semantic_engine or self.semantic_engine.get_index_size() == 0:
            logger.warning("Semantic engine not available")
            return []
        
        try:
            results = self.semantic_engine.search_similar(text, top_k=5)
            return [
                {
                    'title': r.get('title', ''),
                    'source': r.get('source', ''),
                    'similarity_score': r.get('similarity_score', 0),
                    'url': r.get('url')
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error getting semantic similarity: {e}")
            return []
    
    @staticmethod
    def _calculate_avg_similarity(similarity_results: List[Dict]) -> float:
        """Calculate average similarity score."""
        if not similarity_results:
            return 0.0
        return np.mean([r.get('similarity_score', 0) for r in similarity_results])
    
    def fetch_url_content(self, url: str) -> Optional[Dict]:
        """Fetch and extract content from URL."""
        try:
            logger.info(f"Fetching content from {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = None
            if soup.find('h1'):
                title = soup.find('h1').get_text()
            elif soup.find('title'):
                title = soup.find('title').get_text()
            
            # Extract content
            content = []
            for paragraph in soup.find_all('p'):
                content.append(paragraph.get_text())
            
            content_text = ' '.join(content)
            
            if not content_text:
                logger.warning("No content extracted from URL")
                return None
            
            return {
                'headline': title,
                'content': content_text,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error fetching URL content: {e}")
            return None
