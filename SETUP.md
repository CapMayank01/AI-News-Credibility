# Setup Guide

## Complete Installation and Configuration

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.11.x
- **Node.js**: 18.x or 20.x
- **RAM**: 8GB minimum (16GB recommended for GPU)
- **Disk Space**: 10GB minimum

### Step 1: Environment Setup

#### Windows

```bash
# Install Anaconda from https://www.anaconda.com/download

# Create environment
conda create -n news_ai python=3.11 -y

# Activate environment
conda activate news_ai

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux

```bash
# Install Anaconda or Miniconda

# Create environment
conda create -n news_ai python=3.11 -y

# Activate environment
conda activate news_ai

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

#### Using SQLite (Local Development)

No additional setup required. SQLite will be created automatically.

#### Using PostgreSQL (Production)

```bash
# Install PostgreSQL (https://www.postgresql.org/download/)

# Create database
createdb news_credibility

# Update .env with connection string
DATABASE_URL=postgresql://user:password@localhost:5432/news_credibility
```

### Step 3: Download Datasets

1. Go to [Kaggle Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)
2. Download `Fake.csv` and `True.csv`
3. Place in `datasets/raw/` directory

### Step 4: Train Models

```bash
# Activate environment
conda activate news_ai

# Run training pipeline
python train.py
```

This will automatically:
- Clean and process data
- Generate visualizations
- Train all ML models
- Create database tables

### Step 5: Backend Setup

```bash
# Navigate to backend
cd backend

# Create .env file
copy .env.example .env
# Or on Linux/Mac: cp .env.example .env

# Edit .env with your settings
# DATABASE_URL, API keys, paths, etc.

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Step 6: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 📊 Training Models

### Automated Training

```bash
# Run complete pipeline
python train.py
```

### Manual Training

```python
from app.utils.data_loader import DataLoader
from app.utils.distilbert_model import DistilBertTrainer

# Phase 1-2: Load and clean data
df = DataLoader.prepare_dataset(
    'datasets/raw/Fake.csv',
    'datasets/raw/True.csv',
    'datasets/processed/processed_news.csv'
)

# Phase 3: EDA
from app.utils.eda_analyzer import EDAAnalyzer
EDAAnalyzer.generate_full_eda(df, './eda_results')

# Phase 5: Train DistilBERT
trainer = DistilBertTrainer()
trainer.train(X_train, y_train, X_val, y_val)
```

## 🐳 Docker Setup (Optional)

```bash
# Build image
docker build -t news-credibility .

# Run container
docker run -p 8000:8000 -p 3000:3000 news-credibility
```

## ✅ Verification

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "models_loaded": {
    "fake_news_model": true,
    "clickbait_model": true,
    "semantic_engine": false
  },
  "database_connected": true
}
```

### Frontend Access

Open `http://localhost:3000` in browser and verify you can:
- Navigate to different pages
- See home page hero section
- Access analyzer, dashboard, history

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000 (backend)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Kill process on port 3000 (frontend)
# Similar commands with port 3000
```

### Model Loading Errors

```bash
# Download models manually
python -c "
from transformers import DistilBertModel
DistilBertModel.from_pretrained('distilbert-base-uncased')
"
```

### Database Connection Error

```bash
# Test connection
python -c "
from backend.app.core.database import engine
print(engine.connect())
"
```

### Module Import Errors

```bash
# Reinstall packages
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

## 📦 Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=sqlite:///./news_credibility.db
SQLALCHEMY_ECHO=False

# API
API_TITLE=AI-Powered News Credibility Assessment
API_VERSION=1.0.0
DEBUG=True

# Models
MODEL_PATH=./ml_models/fake_news_model/best_model.pt
CLICKBAIT_MODEL_PATH=./ml_models/clickbait_model/clickbait_model.pkl
FAISS_INDEX_PATH=./faiss_index/news_index.faiss
EMBEDDER_MODEL=all-MiniLM-L6-v2

# ML Configuration
MAX_SEQUENCE_LENGTH=512
BATCH_SIZE=32
DEVICE=cpu

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# Source Credibility
SOURCE_CREDIBILITY_PATH=./backend/app/data/source_credibility.json
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Production Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
# Create Heroku app
heroku create news-credibility-api

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main
```

### AWS EC2 Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed AWS setup

## 📈 Performance Optimization

### Backend

```env
# Use production ASGI server
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Enable caching
REDIS_URL=redis://localhost:6379

# Use GPU for inference
DEVICE=cuda
```

### Frontend

```bash
# Production build
npm run build
npm start

# Export static site
npm run export
```

## 📚 Additional Resources

- [Python 3.11 Docs](https://docs.python.org/3.11/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PyTorch Documentation](https://pytorch.org/docs/)

## ✨ Next Steps

1. ✅ Complete setup from this guide
2. 📊 Train models with `python train.py`
3. 🚀 Start backend server
4. 🎨 Start frontend application
5. 📈 Visit http://localhost:3000
6. 🧪 Test with sample articles
7. 📋 Check API docs at http://localhost:8000/docs

## 🆘 Getting Help

- Check [troubleshooting section](#troubleshooting)
- Review [README.md](./README.md)
- Open GitHub issues
- Check API documentation at /docs endpoint
