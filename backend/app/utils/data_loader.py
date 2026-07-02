"""
PHASE 1: DATA COLLECTION
Handles loading and processing of fake and real news datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles dataset loading and preprocessing."""
    
    @staticmethod
    def load_fake_news(filepath: str) -> pd.DataFrame:
        """Load fake news dataset."""
        logger.info(f"Loading fake news from {filepath}")
        df = pd.read_csv(filepath)
        df['label'] = 0  # Fake = 0
        logger.info(f"Loaded {len(df)} fake news articles")
        return df
    
    @staticmethod
    def load_real_news(filepath: str) -> pd.DataFrame:
        """Load real news dataset."""
        logger.info(f"Loading real news from {filepath}")
        df = pd.read_csv(filepath)
        df['label'] = 1  # Real = 1
        logger.info(f"Loaded {len(df)} real news articles")
        return df
    
    @staticmethod
    def merge_datasets(fake_df: pd.DataFrame, real_df: pd.DataFrame) -> pd.DataFrame:
        """Merge fake and real news datasets."""
        logger.info("Merging datasets...")
        merged_df = pd.concat([fake_df, real_df], ignore_index=True)
        logger.info(f"Merged dataset size: {len(merged_df)}")
        return merged_df
    
    @staticmethod
    def shuffle_dataset(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
        """Shuffle the dataset."""
        logger.info("Shuffling dataset...")
        df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)
        return df
    
    @staticmethod
    def prepare_dataset(
        fake_csv: str,
        real_csv: str,
        output_path: str = None,
        shuffle: bool = True,
        random_state: int = 42
    ) -> pd.DataFrame:
        """
        Complete data preparation pipeline.
        
        Args:
            fake_csv: Path to fake news CSV
            real_csv: Path to real news CSV
            output_path: Path to save processed dataset
            shuffle: Whether to shuffle the dataset
            random_state: Random seed for reproducibility
            
        Returns:
            Processed DataFrame
        """
        # Load datasets
        fake_df = DataLoader.load_fake_news(fake_csv)
        real_df = DataLoader.load_real_news(real_csv)
        
        # Merge
        merged_df = DataLoader.merge_datasets(fake_df, real_df)
        
        # Shuffle
        if shuffle:
            merged_df = DataLoader.shuffle_dataset(merged_df, random_state)
        
        # Select relevant columns
        if 'title' in merged_df.columns and 'text' in merged_df.columns:
            merged_df = merged_df[['title', 'text', 'label']]
        elif 'content' in merged_df.columns:
            merged_df = merged_df[['title', 'content', 'label']].rename(columns={'content': 'text'})
        
        # Save if output path provided
        if output_path:
            logger.info(f"Saving processed dataset to {output_path}")
            merged_df.to_csv(output_path, index=False)
            logger.info("Saved successfully!")
        
        # Print statistics
        logger.info(f"\nDataset Statistics:")
        logger.info(f"Total samples: {len(merged_df)}")
        logger.info(f"Fake news (0): {(merged_df['label'] == 0).sum()}")
        logger.info(f"Real news (1): {(merged_df['label'] == 1).sum()}")
        logger.info(f"Class distribution:\n{merged_df['label'].value_counts()}")
        
        return merged_df
    
    @staticmethod
    def load_processed_dataset(filepath: str) -> pd.DataFrame:
        """Load already processed dataset."""
        logger.info(f"Loading processed dataset from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} articles")
        return df
    
    @staticmethod
    def get_data_splits(
        df: pd.DataFrame,
        train_size: float = 0.7,
        val_size: float = 0.15,
        test_size: float = 0.15,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split dataset into train, validation, and test sets."""
        np.random.seed(random_state)
        
        train_df = df.sample(frac=train_size, random_state=random_state)
        remaining = df.drop(train_df.index)
        
        val_test_ratio = val_size / (val_size + test_size)
        val_df = remaining.sample(frac=val_test_ratio, random_state=random_state)
        test_df = remaining.drop(val_df.index)
        
        logger.info(f"Train size: {len(train_df)}")
        logger.info(f"Validation size: {len(val_df)}")
        logger.info(f"Test size: {len(test_df)}")
        
        return train_df, val_df, test_df
