"""
PHASE 4: BASELINE MODEL
TF-IDF + Logistic Regression baseline implementation.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import logging
from pathlib import Path
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaselineModel:
    """TF-IDF + Logistic Regression baseline model."""
    
    def __init__(self, max_features: int = 5000):
        self.vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict:
        """Train the baseline model."""
        logger.info("Training baseline model...")
        
        # Vectorize text
        X_train_vec = self.vectorizer.fit_transform(X_train)
        
        # Train logistic regression
        self.model.fit(X_train_vec, y_train)
        self.is_trained = True
        
        logger.info("Baseline model trained!")
        return {'status': 'trained'}
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        X_vec = self.vectorizer.transform(X)
        return self.model.predict(X_vec)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities."""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        X_vec = self.vectorizer.transform(X)
        return self.model.predict_proba(X_vec)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate model on test set."""
        predictions = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions),
            'recall': recall_score(y_test, predictions),
            'f1': f1_score(y_test, predictions),
            'confusion_matrix': confusion_matrix(y_test, predictions).tolist()
        }
        
        logger.info(f"Baseline Model Results:")
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
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """Load model and vectorizer."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        self.vectorizer = model_data['vectorizer']
        self.model = model_data['model']
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")


def train_baseline_model(
    processed_csv: str,
    output_model_path: str,
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict:
    """
    Complete baseline training pipeline.
    
    Args:
        processed_csv: Path to processed dataset
        output_model_path: Path to save model
        test_size: Test set proportion
        random_state: Random seed
        
    Returns:
        Training results
    """
    logger.info("=" * 50)
    logger.info("BASELINE MODEL TRAINING")
    logger.info("=" * 50)
    
    # Load data
    df = pd.read_csv(processed_csv)
    X = df['text'].fillna('')
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Create and train model
    baseline = BaselineModel()
    baseline.train(X_train.values, y_train.values)
    
    # Evaluate
    results = baseline.evaluate(X_test.values, y_test.values)
    
    # Save model
    baseline.save(output_model_path)
    
    logger.info("=" * 50)
    logger.info("BASELINE MODEL TRAINING COMPLETE")
    logger.info("=" * 50)
    
    return results
