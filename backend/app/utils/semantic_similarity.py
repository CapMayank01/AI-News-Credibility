"""
PHASE 8: SEMANTIC SIMILARITY ENGINE
Uses FAISS for semantic search and similarity matching.
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SemanticSimilarityEngine:
    """Semantic search engine using FAISS and sentence transformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', device: str = 'cpu'):
        logger.info(f"Loading sentence transformer model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self.index = None
        self.articles = []
        self.embeddings = None
    
    def add_articles(self, articles: List[Dict]):
        """
        Add articles to the index.
        
        Args:
            articles: List of article dicts with 'title', 'content', 'source'
        """
        logger.info(f"Adding {len(articles)} articles to index...")
        
        self.articles = articles
        texts = [f"{article.get('title', '')} {article.get('content', '')}" 
                for article in articles]
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Create FAISS index
        logger.info("Creating FAISS index...")
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings.astype('float32'))
        
        logger.info(f"FAISS index created with {len(self.articles)} articles")
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar articles.
        
        Args:
            query: Query text
            top_k: Number of top results
            
        Returns:
            List of similar articles with similarity scores
        """
        if self.index is None:
            raise ValueError("No articles indexed yet")
        
        # Encode query
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        query_embedding = np.array([query_embedding], dtype='float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.articles):
                stored_article = self.articles[idx]
                article = (stored_article.copy() if isinstance(stored_article, dict)
                           else {'title': '', 'content': str(stored_article), 'source': ''})
                # Convert distance to similarity score (0-100)
                similarity = max(0, 100 - (dist * 10))
                article['similarity_score'] = float(similarity)
                results.append(article)
        
        return results
    
    def save_index(self, filepath: str):
        """Save FAISS index and articles."""
        data = {
            'index': self.index,
            'articles': self.articles,
            'embeddings': self.embeddings
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Saved index to {filepath}")
    
    def load_index(self, filepath: str, articles_path: str = None):
        """Load FAISS index and articles."""
        if Path(filepath).suffix == '.faiss':
            if not articles_path:
                raise ValueError("articles_path is required")
            self.index = faiss.read_index(filepath)
            with open(articles_path, 'rb') as f:
                self.articles = pickle.load(f)
            self.embeddings = None
            logger.info(f"Loaded index from {filepath} with {len(self.articles)} articles")
            return
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        self.index = data['index']
        self.articles = data['articles']
        self.embeddings = data['embeddings']
        logger.info(f"Loaded index from {filepath} with {len(self.articles)} articles")
    
    def get_index_size(self) -> int:
        """Get number of articles in index."""
        return len(self.articles) if self.index is not None else 0


def initialize_semantic_engine_from_csv(
    csv_path: str,
    model_name: str = 'all-MiniLM-L6-v2'
) -> SemanticSimilarityEngine:
    """Initialize semantic engine from CSV of trusted articles."""
    
    logger.info(f"Initializing semantic engine from {csv_path}")
    
    # Load articles
    df = pd.read_csv(csv_path)
    articles = df.to_dict('records')
    
    # Create engine
    engine = SemanticSimilarityEngine(model_name=model_name)
    engine.add_articles(articles)
    
    return engine
