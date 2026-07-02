"""
PHASE 7: SOURCE CREDIBILITY ENGINE
Maintains and manages source credibility scores.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SourceCredibilityEngine:
    """Manages source credibility database."""
    
    # Default credibility scores
    DEFAULT_SOURCES = {
        'reuters.com': 99,
        'bbc.com': 95,
        'apnews.com': 98,
        'thehindu.com': 90,
        'indianexpress.com': 88,
        'theguardian.com': 92,
        'nytimes.com': 94,
        'wsj.com': 93,
        'ft.com': 92,
        'thewire.in': 85,
        'ndtv.com': 80,
        'timesofindia.com': 75
    }
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self.sources = self.DEFAULT_SOURCES.copy()
        
        # Load from file if exists
        if db_path and Path(db_path).exists():
            self.load_from_file(db_path)
    
    def get_credibility_score(self, url: str) -> Dict:
        """
        Get credibility score for a given URL.
        
        Args:
            url: Article URL or domain
            
        Returns:
            Credibility score and confidence
        """
        domain = self._extract_domain(url)
        
        # Exact match
        if domain in self.sources:
            score = self.sources[domain]
            return {
                'domain': domain,
                'credibility_score': score,
                'confidence': 100,
                'status': 'known'
            }
        
        # Check for subdomain match
        for known_domain, score in self.sources.items():
            if domain.endswith(known_domain):
                return {
                    'domain': domain,
                    'credibility_score': score,
                    'confidence': 80,
                    'status': 'subdomain_match'
                }
        
        # Unknown source
        return {
            'domain': domain,
            'credibility_score': 50,
            'confidence': 0,
            'status': 'unknown'
        }
    
    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain from URL."""
        import re
        
        # Remove protocol
        url = re.sub(r'https?://', '', url)
        
        # Remove www if present
        url = re.sub(r'^www\.', '', url)
        
        # Extract domain (before first /)
        domain = url.split('/')[0]
        
        return domain.lower()
    
    def add_source(self, domain: str, score: int, overwrite: bool = False) -> bool:
        """Add or update a source."""
        if domain in self.sources and not overwrite:
            logger.warning(f"Source {domain} already exists. Use overwrite=True to update.")
            return False
        
        if not (0 <= score <= 100):
            logger.error("Score must be between 0 and 100")
            return False
        
        self.sources[domain] = score
        logger.info(f"Added/Updated source: {domain} with score {score}")
        return True
    
    def save_to_file(self, filepath: str):
        """Save sources to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.sources, f, indent=2)
        logger.info(f"Saved {len(self.sources)} sources to {filepath}")
    
    def load_from_file(self, filepath: str):
        """Load sources from JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.sources = json.load(f)
            logger.info(f"Loaded {len(self.sources)} sources from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load sources: {e}")
    
    def get_all_sources(self) -> Dict:
        """Get all sources."""
        return self.sources.copy()
    
    def get_source_count(self) -> int:
        """Get number of known sources."""
        return len(self.sources)


def initialize_source_credibility_engine(db_path: str = None) -> SourceCredibilityEngine:
    """Initialize the source credibility engine."""
    engine = SourceCredibilityEngine(db_path)
    logger.info(f"Initialized source credibility engine with {engine.get_source_count()} sources")
    return engine
