"""
PHASE 2: DATA CLEANING
Text cleaning and preprocessing utilities for news articles.
"""

import re
import string
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextCleaner:
    """Handles all text cleaning and preprocessing operations."""
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        url_pattern = r'https?://\S+|www\.\S+'
        return re.sub(url_pattern, '', text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Remove HTML tags from text."""
        html_pattern = r'<[^>]+>'
        return re.sub(html_pattern, '', text)
    
    @staticmethod
    def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
        """
        Remove special characters from text.
        Optionally keeps punctuation relevant to meaning.
        """
        if keep_punctuation:
            # Keep only alphanumeric, spaces, and meaningful punctuation
            pattern = r'[^a-zA-Z0-9\s.,!?;:\'\"-]'
        else:
            # Remove all special characters
            pattern = r'[^a-zA-Z0-9\s]'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """Remove extra spaces and normalize whitespace."""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing spaces
        return text.strip()
    
    @staticmethod
    def lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    @staticmethod
    def remove_numbers(text: str) -> str:
        """Remove numbers from text."""
        return re.sub(r'\d+', '', text)
    
    @staticmethod
    def remove_stopwords(text: str, language: str = 'english') -> str:
        """Remove common stopwords."""
        stop_words = set(stopwords.words(language))
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    
    @staticmethod
    def clean_pipeline(
        text: str,
        remove_urls: bool = True,
        remove_html: bool = True,
        remove_special: bool = True,
        keep_punctuation: bool = True,
        lowercase_text: bool = True,
        remove_nums: bool = False,
        remove_stops: bool = False,
        normalize_spaces: bool = True
    ) -> str:
        """
        Apply full cleaning pipeline to text.
        
        Args:
            text: Input text to clean
            remove_urls: Remove URL patterns
            remove_html: Remove HTML tags
            remove_special: Remove special characters
            keep_punctuation: Keep meaningful punctuation
            lowercase_text: Convert to lowercase
            remove_nums: Remove numbers
            remove_stops: Remove stopwords
            normalize_spaces: Remove extra spaces
            
        Returns:
            Cleaned text
        """
        if remove_urls:
            text = TextCleaner.remove_urls(text)
        
        if remove_html:
            text = TextCleaner.remove_html_tags(text)
        
        if remove_special:
            text = TextCleaner.remove_special_characters(text, keep_punctuation)
        
        if normalize_spaces:
            text = TextCleaner.remove_extra_spaces(text)
        
        if lowercase_text:
            text = TextCleaner.lowercase(text)
        
        if remove_nums:
            text = TextCleaner.remove_numbers(text)
        
        if remove_stops:
            text = TextCleaner.remove_stopwords(text)
        
        return text
    
    @staticmethod
    def clean_batch(texts: List[str], **kwargs) -> List[str]:
        """Clean multiple texts at once."""
        return [TextCleaner.clean_pipeline(text, **kwargs) for text in texts]
