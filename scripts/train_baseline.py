import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "processed" / "combined_data.csv"
MODEL_DIR = ROOT / "ml_models"

def main():
    print("Training baseline model...")
    df = pd.read_csv(DATA)
    X = df['content'].fillna('')
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    X_test_vec = vectorizer.transform(X_test)
    preds = model.predict(X_test_vec)
    acc = (preds == y_test).mean()
    print(f"Baseline model accuracy: {acc:.4f}")
    
    # Save model and vectorizer separately using joblib
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "baseline_model.joblib")
    joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.joblib")
    print("Baseline model and vectorizer saved successfully!")

if __name__ == "__main__":
    main()
