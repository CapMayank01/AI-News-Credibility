"""
PHASE 9: RELIABILITY SCORING SYSTEM
Composite scoring system combining multiple signals.
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReliabilityScorer:
    """Combines multiple signals into a reliability score."""
    
    # Weights for each component (must sum to 1.0)
    WEIGHTS = {
        'model_confidence': 0.5,
        'source_credibility': 0.2,
        'similarity_score': 0.2,
        'clickbait_penalty': 0.1
    }
    
    # Thresholds for classification
    THRESHOLDS = {
        'highly_reliable': 80,
        'reliable': 60,
        'questionable': 40,
        'likely_fake': 0
    }
    
    @staticmethod
    def calculate_score(
        model_confidence: float,
        source_credibility: float,
        average_similarity: float,
        clickbait_probability: float
    ) -> Dict:
        """
        Calculate reliability score using weighted formula.
        
        Formula:
        Reliability = 0.5 × Model Confidence +
                     0.2 × Source Credibility +
                     0.2 × Similarity Score +
                     0.1 × (1 - Clickbait Probability)
        
        Args:
            model_confidence: Model confidence (0-100)
            source_credibility: Source credibility score (0-100)
            average_similarity: Average similarity with trusted articles (0-100)
            clickbait_probability: Probability of being clickbait (0-1)
            
        Returns:
            Reliability score and classification
        """
        # Normalize inputs to 0-100 range if needed
        model_confidence = max(0, min(100, model_confidence))
        source_credibility = max(0, min(100, source_credibility))
        average_similarity = max(0, min(100, average_similarity))
        clickbait_probability = max(0, min(1, clickbait_probability))
        
        # Calculate clickbait component (inverse: lower clickbait = higher score)
        clickbait_component = (1 - clickbait_probability) * 100
        
        # Calculate weighted score
        reliability_score = (
            ReliabilityScorer.WEIGHTS['model_confidence'] * model_confidence +
            ReliabilityScorer.WEIGHTS['source_credibility'] * source_credibility +
            ReliabilityScorer.WEIGHTS['similarity_score'] * average_similarity +
            ReliabilityScorer.WEIGHTS['clickbait_penalty'] * clickbait_component
        )
        
        # Ensure score is in 0-100 range
        reliability_score = max(0, min(100, reliability_score))
        
        # Classify
        classification = ReliabilityScorer._classify_reliability(reliability_score)
        
        return {
            'reliability_score': round(reliability_score, 2),
            'classification': classification,
            'confidence_level': ReliabilityScorer._get_confidence_level(reliability_score),
            'component_breakdown': {
                'model_confidence': model_confidence,
                'source_credibility': source_credibility,
                'similarity_score': average_similarity,
                'clickbait_score': clickbait_probability * 100
            }
        }
    
    @staticmethod
    def _classify_reliability(score: float) -> str:
        """Classify reliability based on score."""
        if score >= ReliabilityScorer.THRESHOLDS['highly_reliable']:
            return 'Highly Reliable'
        elif score >= ReliabilityScorer.THRESHOLDS['reliable']:
            return 'Reliable'
        elif score >= ReliabilityScorer.THRESHOLDS['questionable']:
            return 'Questionable'
        else:
            return 'Likely Fake'
    
    @staticmethod
    def _get_confidence_level(score: float) -> str:
        """Get confidence level description."""
        if score >= 90:
            return 'Very High'
        elif score >= 75:
            return 'High'
        elif score >= 60:
            return 'Medium'
        elif score >= 40:
            return 'Low'
        else:
            return 'Very Low'
    
    @staticmethod
    def get_recommendation(reliability_score: float) -> str:
        """Get recommendation based on score."""
        if reliability_score >= 80:
            return 'This article appears to be reliable. You can share it with confidence.'
        elif reliability_score >= 60:
            return 'This article seems mostly reliable, but verify with additional sources.'
        elif reliability_score >= 40:
            return 'Be cautious with this article. Cross-check with trusted sources.'
        else:
            return 'This article appears to be unreliable or fake. Do not share without verification.'
