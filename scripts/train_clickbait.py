"""Retrain the clickbait model with class-imbalance handling and save metrics."""
import json
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "processed" / "combined_data.csv"
MODEL_DIR = ROOT / "ml_models"
METRICS_DIR = ROOT / "metrics"


def clean(text):
    text = re.sub(r"https?://\S+|www\.\S+", "", str(text))
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def heuristic_label(headline):
    raw = str(headline)
    score = 0
    score += 2 if raw.count("!") > 1 or raw.count("?") > 1 else 0
    score += 2 if sum(1 for word in raw.split() if word.isupper() and len(word) > 1) > 2 else 0
    score += 1 if any(char.isdigit() for char in raw) else 0
    keywords = ("shocking", "unbelievable", "exclusive", "breaking", "viral",
                "trending", "amazing", "incredible", "stunning")
    score += 2 if any(word in raw.lower() for word in keywords) else 0
    return int(score >= 3)


def main():
    frame = pd.read_csv(DATA)
    headlines = frame["headline"].fillna("")
    labels = headlines.map(heuristic_label).to_numpy()
    cleaned = headlines.map(clean).to_numpy()
    x_train, x_test, y_train, y_test = train_test_split(
        cleaned, labels, test_size=0.2, random_state=42, stratify=labels
    )
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=2)
    train_vectors = vectorizer.fit_transform(x_train)
    model = LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced")
    model.fit(train_vectors, y_train)
    predictions = model.predict(vectorizer.transform(x_test))
    metrics = {
        "label_source": "headline heuristic; replace with a human-labelled clickbait dataset",
        "samples": int(len(labels)),
        "positive_samples": int(labels.sum()),
        "test_samples": int(len(y_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    }
    MODEL_DIR.mkdir(exist_ok=True)
    METRICS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "clickbait_model.joblib")
    joblib.dump(vectorizer, MODEL_DIR / "clickbait_tfidf.joblib")
    (METRICS_DIR / "clickbait_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
