"""
Utils __init__.py
"""

from .text_cleaner import TextCleaner
from .data_loader import DataLoader
from .baseline_model import BaselineModel
from .clickbait_detector import ClickbaitDetector
from .source_credibility import SourceCredibilityEngine
from .reliability_scorer import ReliabilityScorer
from .explainability import ExplainabilityModule

# Heavy dependencies wrapped in try-except for lightweight deployment
try:
    from .eda_analyzer import EDAAnalyzer
except ImportError:
    EDAAnalyzer = None

try:
    from .distilbert_model import DistilBertTrainer
except ImportError:
    DistilBertTrainer = None

try:
    from .semantic_similarity import SemanticSimilarityEngine
except ImportError:
    SemanticSimilarityEngine = None

__all__ = [
    'TextCleaner',
    'DataLoader',
    'EDAAnalyzer',
    'BaselineModel',
    'DistilBertTrainer',
    'ClickbaitDetector',
    'SourceCredibilityEngine',
    'SemanticSimilarityEngine',
    'ReliabilityScorer',
    'ExplainabilityModule'
]
