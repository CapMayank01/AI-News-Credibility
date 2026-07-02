"""
PHASE 6: CLICKBAIT DETECTION
Separate model for detecting clickbait headlines.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import logging
from typing import Dict
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClickbaitDetector:
    """Logistic Regression based clickbait detector."""
    
    def __init__(self, max_features: int = 3000):
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict:
        """Train clickbait detector."""
        logger.info("Training clickbait detector...")
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.model.fit(X_train_vec, y_train)
        self.is_trained = True
        
        logger.info("Clickbait detector trained!")
        return {'status': 'trained'}
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get clickbait probability."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        X_vec = self.vectorizer.transform(X)
        probs = self.model.predict_proba(X_vec)
        # Return probability of being clickbait (class 1)
        return probs[:, 1]
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate clickbait detector."""
        X_test_vec = self.vectorizer.transform(X_test)
        predictions = self.model.predict(X_test_vec)
        
        metrics = {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions),
            'recall': recall_score(y_test, predictions),
            'f1': f1_score(y_test, predictions)
        }
        
        logger.info(f"Clickbait Detector Results:")
        logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall: {metrics['recall']:.4f}")
        logger.info(f"  F1-Score: {metrics['f1']:.4f}")
        
        return metrics
    
    def save(self, filepath: str):
        """Save model and vectorizer."""
        model_data = {
            'vectorizer': self.vectorizer,
            'model': self.model
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        logger.info(f"Clickbait model saved to {filepath}")
    
    def load(self, filepath: str, vectorizer_path: str = None):
        """Load model and vectorizer."""
        if vectorizer_path:
            self.model = joblib.load(filepath)
            self.vectorizer = joblib.load(vectorizer_path)
        else:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            self.vectorizer = model_data['vectorizer']
            self.model = model_data['model']
        self.is_trained = True
        logger.info(f"Clickbait model loaded from {filepath}")


def detect_clickbait(text: str, detector: ClickbaitDetector) -> Dict:
    """
    Detect clickbait in a single article.
    
    Args:
        text: Article text
        detector: Trained ClickbaitDetector instance
        
    Returns:
        Clickbait detection result with probability
    """
    probability = detector.predict_proba(np.array([text]))[0]
    
    return {
        'is_clickbait_probability': float(probability),
        'clickbait_score': float(probability) * 100,
        'classification': 'Likely Clickbait' if probability > 0.5 else 'Not Clickbait'
    }
