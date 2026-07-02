"""
PHASE 3: EXPLORATORY DATA ANALYSIS (EDA)
Generates insights and visualizations from the dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EDAAnalyzer:
    """Performs exploratory data analysis on news dataset."""
    
    @staticmethod
    def class_distribution(df: pd.DataFrame, save_path: str = None) -> Dict:
        """Analyze class distribution."""
        logger.info("Analyzing class distribution...")
        
        fake_count = (df['label'] == 0).sum()
        real_count = (df['label'] == 1).sum()
        
        stats = {
            'fake_count': fake_count,
            'real_count': real_count,
            'fake_percentage': (fake_count / len(df)) * 100,
            'real_percentage': (real_count / len(df)) * 100
        }
        
        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        classes = ['Fake News', 'Real News']
        counts = [fake_count, real_count]
        colors = ['#ff6b6b', '#4ecdc4']
        
        bars = ax.bar(classes, counts, color=colors)
        ax.set_ylabel('Number of Articles')
        ax.set_title('Class Distribution')
        ax.set_ylim(0, max(counts) * 1.1)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({int(height)/len(df)*100:.1f}%)',
                   ha='center', va='bottom')
        
        if save_path:
            plt.savefig(f'{save_path}/class_distribution.png', dpi=300, bbox_inches='tight')
            logger.info(f"Saved class distribution plot")
        plt.close()
        
        return stats
    
    @staticmethod
    def word_count_distribution(df: pd.DataFrame, save_path: str = None) -> Dict:
        """Analyze word count distribution."""
        logger.info("Analyzing word count distribution...")
        
        df['word_count'] = df['text'].fillna('').str.split().str.len()
        
        stats = {
            'mean_words': df['word_count'].mean(),
            'median_words': df['word_count'].median(),
            'min_words': df['word_count'].min(),
            'max_words': df['word_count'].max(),
            'std_words': df['word_count'].std()
        }
        
        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Overall distribution
        axes[0].hist(df['word_count'], bins=50, color='#3498db', edgecolor='black')
        axes[0].set_xlabel('Word Count')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Overall Word Count Distribution')
        axes[0].axvline(stats['mean_words'], color='red', linestyle='--', label='Mean')
        axes[0].axvline(stats['median_words'], color='green', linestyle='--', label='Median')
        axes[0].legend()
        
        # By class
        fake_words = df[df['label'] == 0]['word_count']
        real_words = df[df['label'] == 1]['word_count']
        axes[1].hist(fake_words, bins=50, alpha=0.6, label='Fake', color='#ff6b6b')
        axes[1].hist(real_words, bins=50, alpha=0.6, label='Real', color='#4ecdc4')
        axes[1].set_xlabel('Word Count')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Word Count Distribution by Class')
        axes[1].legend()
        
        if save_path:
            plt.savefig(f'{save_path}/word_count_distribution.png', dpi=300, bbox_inches='tight')
            logger.info("Saved word count distribution plot")
        plt.close()
        
        return stats
    
    @staticmethod
    def top_words(df: pd.DataFrame, n_words: int = 20, save_path: str = None):
        """Find and visualize top words."""
        logger.info(f"Finding top {n_words} words...")
        
        # Overall top words
        all_words = ' '.join(df['text'].fillna('').astype(str)).lower().split()
        top_words_all = Counter(all_words).most_common(n_words)
        
        # Fake news top words
        fake_texts = ' '.join(df[df['label'] == 0]['text'].fillna('').astype(str)).lower().split()
        top_words_fake = Counter(fake_texts).most_common(n_words)
        
        # Real news top words
        real_texts = ' '.join(df[df['label'] == 1]['text'].fillna('').astype(str)).lower().split()
        top_words_real = Counter(real_texts).most_common(n_words)
        
        # Visualization
        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        
        # All words
        words, counts = zip(*top_words_all)
        axes[0].barh(words, counts, color='#3498db')
        axes[0].set_xlabel('Frequency')
        axes[0].set_title('Top Words - Overall')
        axes[0].invert_yaxis()
        
        # Fake news
        words, counts = zip(*top_words_fake)
        axes[1].barh(words, counts, color='#ff6b6b')
        axes[1].set_xlabel('Frequency')
        axes[1].set_title('Top Words - Fake News')
        axes[1].invert_yaxis()
        
        # Real news
        words, counts = zip(*top_words_real)
        axes[2].barh(words, counts, color='#4ecdc4')
        axes[2].set_xlabel('Frequency')
        axes[2].set_title('Top Words - Real News')
        axes[2].invert_yaxis()
        
        if save_path:
            plt.savefig(f'{save_path}/top_words.png', dpi=300, bbox_inches='tight')
            logger.info("Saved top words plot")
        plt.close()
        
        return {
            'top_words_all': top_words_all,
            'top_words_fake': top_words_fake,
            'top_words_real': top_words_real
        }
    
    @staticmethod
    def generate_full_eda(df: pd.DataFrame, save_dir: str = './eda_results'):
        """Generate complete EDA report."""
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        logger.info("=" * 50)
        logger.info("GENERATING COMPLETE EDA REPORT")
        logger.info("=" * 50)
        
        # Class distribution
        class_stats = EDAAnalyzer.class_distribution(df, save_dir)
        logger.info(f"\nClass Distribution: {class_stats}")
        
        # Word count distribution
        word_stats = EDAAnalyzer.word_count_distribution(df, save_dir)
        logger.info(f"\nWord Count Statistics: {word_stats}")
        
        # Top words
        top_words_data = EDAAnalyzer.top_words(df, n_words=20, save_path=save_dir)
        
        logger.info("=" * 50)
        logger.info("EDA REPORT GENERATED")
        logger.info("=" * 50)
        
        return {
            'class_distribution': class_stats,
            'word_count': word_stats,
            'top_words': top_words_data
        }
