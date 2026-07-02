# Development Instructions

## Project Setup Quick Reference

### 1. Environment Activation

```bash
conda activate news_ai
```

### 2. Backend Launch

```bash
cd backend
uvicorn app.main:app --reload
# Runs on: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 3. Frontend Launch

```bash
cd frontend
npm run dev
# Runs on: http://localhost:3000
```

### 4. Training Models

```bash
python train.py
```

## Project Structure Map

```
AI-News-Credibility/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app & endpoints
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Request/response schemas
│   │   ├── services/          # Business logic
│   │   ├── utils/             # ML utilities
│   │   │   ├── data_loader.py          # Data loading (Phase 1)
│   │   │   ├── text_cleaner.py         # Data cleaning (Phase 2)
│   │   │   ├── eda_analyzer.py         # EDA (Phase 3)
│   │   │   ├── baseline_model.py       # Baseline model (Phase 4)
│   │   │   ├── distilbert_model.py     # DistilBERT (Phase 5)
│   │   │   ├── clickbait_detector.py   # Clickbait detection (Phase 6)
│   │   │   ├── source_credibility.py   # Source engine (Phase 7)
│   │   │   ├── semantic_similarity.py  # Semantic search (Phase 8)
│   │   │   ├── reliability_scorer.py   # Scoring (Phase 9)
│   │   │   ├── explainability.py       # SHAP explanations (Phase 10)
│   │   ├── core/
│   │   │   ├── config.py      # Settings
│   │   │   └── database.py    # DB configuration
│   │   └── data/
│   │       └── source_credibility.json
│   └── requirements.txt
├── frontend/                   # Next.js application
│   ├── src/
│   │   ├── app/               # Pages
│   │   │   ├── page.tsx       # Home page
│   │   │   ├── analyzer/      # Analyzer page
│   │   │   ├── dashboard/     # Dashboard page
│   │   │   ├── history/       # History page
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript types
│   ├── package.json
│   └── tailwind.config.ts
├── datasets/
│   ├── raw/                   # Original Kaggle data
│   └── processed/             # Cleaned data
├── ml_models/                 # Trained models
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentation
├── train.py                   # Training script
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment
└── README.md                  # Main documentation
```

## Key Files

### ML Utilities (backend/app/utils/)
- **data_loader.py**: Load and prepare Kaggle datasets
- **text_cleaner.py**: Clean and normalize text
- **eda_analyzer.py**: Generate visualizations and statistics
- **baseline_model.py**: TF-IDF baseline implementation
- **distilbert_model.py**: BERT fine-tuning for classification
- **clickbait_detector.py**: Detect clickbait headlines
- **source_credibility.py**: Manage trusted sources
- **semantic_similarity.py**: FAISS semantic search
- **reliability_scorer.py**: Calculate composite scores
- **explainability.py**: SHAP-based interpretability

### API Endpoints (backend/app/main.py)
- `POST /analyze-text`: Analyze article text
- `POST /analyze-url`: Analyze URL
- `GET /history`: Get analysis history
- `GET /dashboard-stats`: Get statistics
- `GET /health`: Health check

### Frontend Pages (frontend/src/app/)
- `/`: Home page with features
- `/analyzer`: Text/URL analysis interface
- `/dashboard`: Analytics and statistics
- `/history`: Previous analyses history

## Common Tasks

### Add New ML Model

1. Create utility class in `backend/app/utils/`
2. Initialize in `analysis_service.py`
3. Add endpoint in `main.py`
4. Add component in frontend

### Add Database Table

1. Create model in `backend/app/models/database.py`
2. Run `init_db()` to create tables
3. Query with `db.query(ModelName)`

### Add Frontend Page

1. Create `.tsx` file in `frontend/src/app/`
2. Use existing components or create new ones
3. Import API services from `services/api.ts`

### Debug Backend

```bash
# Run with debug logging
export DEBUG=True
uvicorn app.main:app --reload --log-level debug
```

### Debug Frontend

```bash
# Browser console logs are visible
# Use React DevTools extension
# Check Network tab for API calls
```

## Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Set `DEBUG=False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up CORS properly
- [ ] Configure rate limiting
- [ ] Add logging and monitoring
- [ ] Test all API endpoints
- [ ] Build frontend: `npm run build`
- [ ] Use production ASGI server (Gunicorn)

## Performance Tips

- Models run faster on GPU: `DEVICE=cuda`
- Cache FAISS index after building
- Use Redis for caching results
- Optimize database queries with indexes
- Compress API responses
- Enable frontend caching

## Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## Documentation Files

- **README.md**: Project overview and quick start
- **SETUP.md**: Detailed setup instructions
- **docs/API.md**: API endpoint documentation
- **docs/MODELS.md**: ML model details
- **docs/DATABASE.md**: Database schema
- **docs/DEPLOYMENT.md**: Production deployment

---

**Last Updated**: 2024
**Project Status**: Production Ready
