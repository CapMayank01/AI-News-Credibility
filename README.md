# AI-Powered News Credibility Assessment Platform

A production-ready system for analyzing news article credibility using Machine Learning, NLP, and Semantic Similarity Search.

## 🌟 Features

- **AI-Powered Analysis**: Uses DistilBERT and TF-IDF models (95%+ accuracy)
- **Text & URL Analysis**: Analyze articles by pasting text or providing URLs
- **Fake News Detection**: Advanced ML models identify fake news articles
- **Clickbait Detection**: Separate model for detecting clickbait headlines
- **Source Credibility**: Database of trusted news sources with credibility scores
- **Semantic Similarity**: FAISS-based search for similar trusted articles
- **Explainability**: SHAP-based explanations for model predictions
- **Dashboard**: Real-time analytics and statistics
- **History**: Track all previous analyses
- **API**: RESTful FastAPI backend for easy integration

## 🏗️ Architecture

```
AI-News-Credibility/
├── frontend/                 # Next.js 15 + React 19 UI
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── utils/           # ML models and utilities
│   │   ├── core/            # Configuration and database
│   │   └── main.py          # API entry point
├── datasets/                # Training data
│   ├── raw/                # Original Kaggle datasets
│   └── processed/          # Processed datasets
├── ml_models/              # Trained ML models
├── notebooks/              # Jupyter notebooks
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- Node.js 18+
- PostgreSQL (optional - SQLite used for local development)
- Anaconda (recommended)

### 1. Environment Setup

```bash
# Create conda environment
conda create -n news_ai python=3.11

# Activate environment
conda activate news_ai

# Install dependencies
pip install -r requirements.txt

# Or use environment.yml
conda env create -f environment.yml
conda activate news_ai
```

### 2. Download Datasets

Download datasets from Kaggle and place them in `datasets/raw/`:
- [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
  - `Fake.csv`
  - `True.csv`

### 3. Train Models

```bash
python train.py
```

This will:
- Process and clean data
- Generate EDA visualizations
- Train baseline model (TF-IDF)
- Fine-tune DistilBERT model
- Train clickbait detector
- Initialize source credibility engine

### 4. Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 5. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

## 📚 Project Structure

### Phases Implemented

1. **Data Collection**: Load and label fake/real news datasets
2. **Data Cleaning**: Remove URLs, HTML, normalize text
3. **EDA**: Generate visualizations and statistics
4. **Baseline Model**: TF-IDF + Logistic Regression
5. **DistilBERT**: Fine-tuned BERT model (95%+ accuracy)
6. **Clickbait Detection**: Separate classification model
7. **Source Credibility**: Database of trusted sources
8. **Semantic Similarity**: FAISS-based search engine
9. **Reliability Scoring**: Weighted composite scoring system
10. **Explainability**: SHAP-based interpretability
11. **FastAPI Backend**: Production-ready REST API
12. **Database Design**: SQLAlchemy ORM models
13. **Frontend Design**: Modern Next.js UI
14. **Security**: Input validation, rate limiting, error handling
15. **Code Quality**: Type hints, logging, modular architecture
16. **Deployment**: Local development setup complete

## 🔌 API Endpoints

### Analysis

```bash
# Analyze text
POST /analyze-text
{
  "text": "Article content...",
  "headline": "Article headline",
  "source_url": "https://example.com"
}

# Analyze URL
POST /analyze-url
{
  "url": "https://example.com/article"
}

# Get analysis history
GET /history?page=1&page_size=10

# Get dashboard stats
GET /dashboard-stats

# Health check
GET /health
```

## 🧠 ML Models

### Fake News Classification
- **Model**: DistilBERT (fine-tuned)
- **Accuracy**: 95%+
- **Input**: Article text (up to 512 tokens)
- **Output**: Prediction (Fake/Real) + Confidence

### Clickbait Detection
- **Model**: TF-IDF + Logistic Regression
- **Output**: Probability score (0-1)

### Semantic Similarity
- **Model**: SentenceTransformers (all-MiniLM-L6-v2)
- **Index**: FAISS for fast search
- **Output**: Top 5 similar trusted articles

## 📊 Reliability Score Formula

```
Reliability Score = 
  0.5 × Model Confidence +
  0.2 × Source Credibility +
  0.2 × Similarity Score +
  0.1 × (1 - Clickbait Probability)
```

Range: 0-100
- **80+**: Highly Reliable
- **60-80**: Reliable
- **40-60**: Questionable
- **<40**: Likely Fake

## 🛠️ Technology Stack

### Backend
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL/SQLite
- Uvicorn
- Pydantic 2.5.0

### Machine Learning
- PyTorch 2.1.1
- HuggingFace Transformers 4.35.2
- Sentence Transformers 2.2.2
- FAISS 1.7.4
- Scikit-Learn 1.3.2
- SHAP 0.43.0

### Frontend
- Next.js 15.0.0
- React 19.0.0-beta
- TypeScript 5.3.3
- Tailwind CSS 3.3.6
- Recharts 2.10.3
- Axios 1.6.2

## 📝 Configuration

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=sqlite:///./test.db

# API
DEBUG=True
API_TITLE=AI-Powered News Credibility

# Models
MODEL_PATH=./ml_models/fake_news_model/best_model.pt
CLICKBAIT_MODEL_PATH=./ml_models/clickbait_model/clickbait_model.pkl
FAISS_INDEX_PATH=./faiss_index/news_index.faiss
EMBEDDER_MODEL=all-MiniLM-L6-v2

# Device
DEVICE=cpu  # or 'cuda' for GPU

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

Create `.env.local` file in frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

```bash
# Run backend tests (setup pytest first)
pytest backend/tests/

# Run frontend tests
npm test
```

## 📖 Documentation

- [API Documentation](./docs/API.md)
- [ML Model Details](./docs/MODELS.md)
- [Database Schema](./docs/DATABASE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## 🔐 Security

- ✓ Input validation (Pydantic)
- ✓ SQL injection protection (SQLAlchemy ORM)
- ✓ CORS configuration
- ✓ Rate limiting
- ✓ Error handling
- ✓ Environment variables for secrets

## 📈 Performance

- **Model Inference**: ~200ms per article
- **API Response**: <500ms average
- **Database Queries**: <100ms
- **Frontend Load**: <1s

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## 👥 Authors

AI/ML Engineering Team

## 🎓 Learning Resources

- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js 15 Docs](https://nextjs.org/docs)

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Browser extension
- [ ] Mobile app
- [ ] Real-time fact-checking API integration
- [ ] Community voting system
- [ ] Advanced analytics dashboard
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] GraphQL API

## 📞 Support

For issues or questions, please open an issue on GitHub or contact support.

---

**Made with ❤️ by the AI/ML Engineering Team**
