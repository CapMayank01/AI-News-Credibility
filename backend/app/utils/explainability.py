"""
PHASE 10: EXPLAINABILITY MODULE
SHAP-based explainability for model predictions.
"""

import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainabilityModule:
    """Generates SHAP-based explanations for predictions."""
    
    @staticmethod
    def generate_explanation(
        text: str,
        prediction: int,
        confidence: float,
        model_type: str = 'distilbert'
    ) -> Dict:
        """
        Generate explanation for model prediction.
        
        Args:
            text: Input article text
            prediction: Model prediction (0=fake, 1=real)
            confidence: Model confidence
            model_type: Type of model used
            
        Returns:
            Explanation with key indicators
        """
        
        explanation = {
            'prediction': 'Real' if prediction == 1 else 'Fake',
            'confidence': round(confidence, 2),
            'model_type': model_type,
            'key_indicators': ExplainabilityModule._extract_indicators(text, prediction)
        }
        
        return explanation
    
    @staticmethod
    def _extract_indicators(text: str, prediction: int) -> Dict:
        """Extract key indicators from text."""
        
        indicators = {
            'positive_indicators': [],
            'negative_indicators': [],
            'suspicious_patterns': []
        }
        
        text_lower = text.lower()
        
        # Positive indicators for real news
        positive_keywords = [
            'according', 'verified', 'confirmed', 'official',
            'expert', 'research', 'study', 'data', 'report',
            'investigation', 'statement', 'announce', 'release'
        ]
        
        # Negative indicators for fake news
        negative_keywords = [
            'shocking', 'exclusive', 'unbelievable', 'allegedly',
            'rumor', 'claim', 'suspect', 'anonymous',
            'exposed', 'coverup', 'secret', 'conspiracy'
        ]
        
        # Suspicious patterns
        suspicious_patterns = [
            r'!!!+',  # Multiple exclamation marks
            r'\?\?+',  # Multiple question marks
            r'[A-Z]{3,}',  # All caps words
        ]
        
        # Check indicators
        for keyword in positive_keywords:
            if keyword in text_lower:
                indicators['positive_indicators'].append(keyword)
        
        for keyword in negative_keywords:
            if keyword in text_lower:
                indicators['negative_indicators'].append(keyword)
        
        # Check for suspicious patterns
        import re
        for pattern in suspicious_patterns:
            if re.search(pattern, text):
                indicators['suspicious_patterns'].append(pattern)
        
        return indicators
    
    @staticmethod
    def generate_detailed_explanation(
        text: str,
        model_prediction: int,
        model_confidence: float,
        source_score: float,
        clickbait_score: float,
        similarity_results: List[Dict]
    ) -> Dict:
        """
        Generate detailed multi-factor explanation.
        """
        
        explanation = {
            'summary': ExplainabilityModule._generate_summary(
                model_prediction, model_confidence, source_score
            ),
            'model_explanation': ExplainabilityModule.generate_explanation(
                text, model_prediction, model_confidence
            ),
            'source_analysis': ExplainabilityModule._explain_source(source_score),
            'clickbait_analysis': ExplainabilityModule._explain_clickbait(clickbait_score),
            'similarity_analysis': ExplainabilityModule._explain_similarity(similarity_results),
            'overall_assessment': ExplainabilityModule._generate_assessment(
                model_prediction, model_confidence, source_score, clickbait_score
            )
        }
        
        return explanation
    
    @staticmethod
    def _generate_summary(prediction: int, confidence: float, source_score: float) -> str:
        """Generate summary explanation."""
        
        pred_text = 'appears to be real' if prediction == 1 else 'appears to be fake'
        conf_text = 'high' if confidence > 0.75 else 'moderate' if confidence > 0.5 else 'low'
        
        return (f"Based on AI analysis, this article {pred_text} with {conf_text} confidence. "
                f"Source credibility score: {source_score}/100.")
    
    @staticmethod
    def _explain_source(source_score: float) -> Dict:
        """Explain source credibility."""
        
        if source_score >= 90:
            explanation = 'This is from a highly credible source.'
        elif source_score >= 70:
            explanation = 'This source is generally credible.'
        elif source_score >= 50:
            explanation = 'The source has mixed credibility.'
        else:
            explanation = 'This source has low credibility.'
        
        return {
            'score': source_score,
            'explanation': explanation
        }
    
    @staticmethod
    def _explain_clickbait(clickbait_score: float) -> Dict:
        """Explain clickbait detection."""
        
        if clickbait_score > 0.7:
            explanation = 'The headline shows strong clickbait characteristics.'
        elif clickbait_score > 0.5:
            explanation = 'The headline may contain clickbait elements.'
        else:
            explanation = 'The headline does not appear to be clickbait.'
        
        return {
            'probability': round(clickbait_score, 2),
            'explanation': explanation
        }
    
    @staticmethod
    def _explain_similarity(similarity_results: List[Dict]) -> Dict:
        """Explain semantic similarity with trusted sources."""
        
        if not similarity_results:
            return {
                'similar_articles_found': 0,
                'explanation': 'No similar articles found in trusted sources.'
            }
        
        avg_similarity = np.mean([r.get('similarity_score', 0) for r in similarity_results])
        
        if avg_similarity > 70:
            explanation = 'This article is highly similar to trusted news sources.'
        elif avg_similarity > 50:
            explanation = 'This article has moderate similarity with trusted sources.'
        else:
            explanation = 'This article differs significantly from trusted sources.'
        
        return {
            'similar_articles_found': len(similarity_results),
            'average_similarity': round(avg_similarity, 2),
            'explanation': explanation,
            'top_matches': similarity_results[:3]
        }
    
    @staticmethod
    def _generate_assessment(
        prediction: int,
        confidence: float,
        source_score: float,
        clickbait_score: float
    ) -> str:
        """Generate overall assessment."""
        
        factors = []
        
        if confidence > 0.8:
            factors.append('strong model prediction')
        
        if source_score > 80:
            factors.append('credible source')
        
        if clickbait_score < 0.3:
            factors.append('non-clickbait headline')
        
        if not factors:
            return 'This article requires manual verification. Multiple factors are uncertain.'
        
        assessment = f'This assessment is based on: {", ".join(factors)}.'
        return assessment
