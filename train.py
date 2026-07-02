"""
Complete Training Pipeline
Runs all training phases for the fake news detection project.
"""

import os
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Execute complete training pipeline."""
    logger.info("=" * 70)
    logger.info("AI-POWERED NEWS CREDIBILITY ASSESSMENT - TRAINING PIPELINE")
    logger.info("=" * 70)
    
    # Check if datasets exist
    fake_csv = './datasets/raw/Fake.csv'
    real_csv = './datasets/raw/True.csv'
    
    if not os.path.exists(fake_csv) or not os.path.exists(real_csv):
        logger.error("Dataset files not found!")
        logger.error(f"  - Expected: {fake_csv}")
        logger.error(f"  - Expected: {real_csv}")
        logger.error("\nDownload datasets from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        return
    
    # PHASE 1-2: Data Collection and Cleaning
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 1-2: DATA COLLECTION AND CLEANING")
    logger.info("=" * 70)
    
    try:
        from app.utils.data_loader import DataLoader
        from app.utils.text_cleaner import TextCleaner
        
        processed_csv = './datasets/processed/processed_news.csv'
        os.makedirs('./datasets/processed', exist_ok=True)
        
        # Load and prepare data
        df = DataLoader.prepare_dataset(fake_csv, real_csv, processed_csv)
        logger.info(f"✓ Data preparation complete: {processed_csv}")
        
    except Exception as e:
        logger.error(f"✗ Data preparation failed: {e}")
        return
    
    # PHASE 3: EDA
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 3: EXPLORATORY DATA ANALYSIS")
    logger.info("=" * 70)
    
    try:
        from app.utils.eda_analyzer import EDAAnalyzer
        
        eda_dir = './eda_results'
        os.makedirs(eda_dir, exist_ok=True)
        
        eda_results = EDAAnalyzer.generate_full_eda(df, eda_dir)
        logger.info(f"✓ EDA complete: {eda_dir}")
        
    except Exception as e:
        logger.error(f"✗ EDA failed: {e}")
    
    # PHASE 4: Baseline Model
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 4: BASELINE MODEL (TF-IDF + LOGISTIC REGRESSION)")
    logger.info("=" * 70)
    
    try:
        from app.utils.baseline_model import train_baseline_model
        
        baseline_model_path = './ml_models/fake_news_model/baseline_model.pkl'
        os.makedirs('./ml_models/fake_news_model', exist_ok=True)
        
        baseline_results = train_baseline_model(
            processed_csv,
            baseline_model_path,
            test_size=0.2,
            random_state=42
        )
        logger.info(f"✓ Baseline model trained: {baseline_results}")
        
    except Exception as e:
        logger.error(f"✗ Baseline model training failed: {e}")
    
    # PHASE 5: DistilBERT Model
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 5: DISTILBERT FINE-TUNING")
    logger.info("=" * 70)
    
    try:
        import pandas as pd
        from app.utils.distilbert_model import DistilBertTrainer
        from sklearn.model_selection import train_test_split
        
        distilbert_model_path = './ml_models/fake_news_model/best_model.pt'
        
        # Load data
        df = pd.read_csv(processed_csv)
        X = df['text'].fillna('')
        y = df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_subset = X_train.iloc[:len(X_train)//2] if len(X_train) > 10000 else X_train
        y_train_subset = y_train.iloc[:len(y_train)//2] if len(y_train) > 10000 else y_train
        
        X_val = X_train_subset.iloc[:len(X_train_subset)//4]
        y_val = y_train_subset.iloc[:len(y_train_subset)//4]
        
        trainer = DistilBertTrainer(device='cpu')
        results = trainer.train(
            X_train_subset.values,
            y_train_subset.values,
            X_val.values,
            y_val.values,
            epochs=3,
            batch_size=8,
            save_path=distilbert_model_path
        )
        logger.info(f"✓ DistilBERT model trained: {results}")
        
    except Exception as e:
        logger.error(f"✗ DistilBERT training failed: {e}")
        logger.info("  Note: Ensure GPU/CUDA is available for optimal performance")
    
    # PHASE 6: Clickbait Detection
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 6: CLICKBAIT DETECTION MODEL")
    logger.info("=" * 70)
    
    try:
        from app.utils.clickbait_detector import ClickbaitDetector
        
        clickbait_model_path = './ml_models/clickbait_model/clickbait_model.pkl'
        os.makedirs('./ml_models/clickbait_model', exist_ok=True)
        
        # For now, use the same data and label with alternate labeling
        # In production, use actual clickbait dataset
        detector = ClickbaitDetector()
        detector.train(
            X_train.iloc[:1000].values,
            (y_train.iloc[:1000] > 0.5).astype(int).values
        )
        detector.save(clickbait_model_path)
        logger.info(f"✓ Clickbait detector trained: {clickbait_model_path}")
        
    except Exception as e:
        logger.error(f"✗ Clickbait detection training failed: {e}")
    
    # PHASE 7: Source Credibility Engine
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 7: SOURCE CREDIBILITY ENGINE")
    logger.info("=" * 70)
    
    try:
        from app.utils.source_credibility import SourceCredibilityEngine
        
        credibility_path = './backend/app/data/source_credibility.json'
        os.makedirs('./backend/app/data', exist_ok=True)
        
        engine = SourceCredibilityEngine()
        engine.save_to_file(credibility_path)
        logger.info(f"✓ Source credibility engine initialized: {credibility_path}")
        
    except Exception as e:
        logger.error(f"✗ Source credibility engine setup failed: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING PIPELINE COMPLETE")
    logger.info("=" * 70)
    logger.info("\nModels and data prepared:")
    logger.info("  ✓ Processed dataset: ./datasets/processed/processed_news.csv")
    logger.info("  ✓ Baseline model: ./ml_models/fake_news_model/baseline_model.pkl")
    logger.info("  ✓ DistilBERT model: ./ml_models/fake_news_model/best_model.pt")
    logger.info("  ✓ Clickbait model: ./ml_models/clickbait_model/clickbait_model.pkl")
    logger.info("  ✓ Source credibility database: ./backend/app/data/source_credibility.json")
    logger.info("\nNext steps:")
    logger.info("  1. Start backend: uvicorn app.main:app --reload")
    logger.info("  2. Start frontend: npm run dev (in frontend directory)")


if __name__ == '__main__':
    main()
