# PIMP - Product Trend Prediction Engine

## Overview

PIMP is an AI-powered product trend prediction engine that combines machine learning, web scraping, and real-time data analysis to identify emerging product trends across Indian e-commerce platforms (Amazon, Flipkart, Meesho) and social media (Reddit, Google Trends).

## Features

### Data Collection
- **E-commerce Scraping**: Automatic data collection from Amazon, Flipkart, and Meesho
- **Social Media Analysis**: Reddit post tracking and sentiment analysis
- **Trend Monitoring**: Real-time Google Trends integration
- **Historical Data**: Complete product history and metric tracking

### Machine Learning
- **Ensemble Predictions**: Combined Random Forest, Gradient Boosting, and Prophet models
- **Feature Engineering**: Temporal, lag, rolling window, and interaction features
- **NLP Sentiment Analysis**: HuggingFace transformers and VADER sentiment analysis
- **Time Series Forecasting**: Prophet-based trend forecasting

### API
- **RESTful API**: FastAPI-powered REST endpoints
- **Real-time Predictions**: Instant trend prediction queries
- **Analytics Dashboard**: Comprehensive analytics and metrics
- **Trending Products**: Top trending products by category

### Infrastructure
- **Docker**: Containerized deployment
- **PostgreSQL**: Robust data persistence
- **Redis**: High-performance caching
- **Nginx**: Load balancing and reverse proxy
- **Airflow**: Automated data pipeline orchestration

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PIMP System                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Data Layer │  │ ML Pipeline  │  │   API Layer  │   │
│  ├─────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ PostgreSQL  │  │ Ensemble     │  │ FastAPI      │   │
│  │ Redis Cache │  │ Predictions  │  │ Endpoints    │   │
│  │ Collections │  │              │  │              │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │        Automation & Scheduling (Airflow)        │   │
│  │  • Scraping • Data Processing • Predictions     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │     Infrastructure (Docker, Nginx, SSL)          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL
- Redis

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/aabc25891-ops/Pimp.git
cd Pimp
```

2. **Set Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access Services**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Airflow: http://localhost:8080
- Nginx: http://localhost (HTTPS)

## API Endpoints

### Products
- `GET /api/v1/products/` - List all products
- `GET /api/v1/products/{id}` - Get product details
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/category/{category}/trending` - Trending in category

### Predictions
- `GET /api/v1/predictions/` - List predictions
- `GET /api/v1/predictions/product/{id}` - Get predictions for product
- `GET /api/v1/predictions/top-trending` - Top trending products
- `POST /api/v1/predictions/` - Create prediction

### Analytics
- `GET /api/v1/analytics/summary` - Analytics summary
- `GET /api/v1/analytics/category-stats` - Statistics by category
- `GET /api/v1/analytics/model-performance` - Model performance metrics
- `GET /api/v1/analytics/api-usage` - API usage statistics

### Trends
- `GET /api/v1/trends/google/trending` - Google trending searches
- `GET /api/v1/trends/reddit/trending` - Reddit trending posts
- `GET /api/v1/trends/keyword/{keyword}` - Keyword trend data
- `GET /api/v1/trends/momentum` - Trend momentum analysis

## Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pimp_db

# Redis
REDIS_URL=redis://localhost:6379/0

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
SECRET_KEY=your-secret-key

# External APIs
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-secret
REDDIT_USER_AGENT=PIMP/1.0

# Settings
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

## Project Structure

```
Pimp/
├── api/                      # FastAPI application
│   ├── main.py              # Main app
│   └── routes/              # API routes
├── data_collection/          # Data scraping & collection
│   ├── scrapers/            # Web scrapers
│   └── apis/                # External API integrations
├── ml_models/               # ML models
│   ├── feature_engineering.py
│   ├── forecasting.py
│   ├── nlp_sentiment.py
│   └── ensemble.py
├── database/                # Database models & migrations
├── automation/              # Airflow DAG & scheduling
├── tests/                   # Unit tests
├── utils/                   # Utilities
├── config/                  # Configuration
├── Dockerfile               # Docker image
├── docker-compose.yml       # Docker compose
├── nginx.conf              # Nginx configuration
└── requirements.txt        # Python dependencies
```

## Development

### Local Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Format code
black .
isort .

# Run linting
flake8 .
mypy .
```

### Running Locally
```bash
# Start FastAPI
uvicorn api.main:app --reload

# Start scheduler
python -c "from automation.scheduler import PIMPScheduler; scheduler = PIMPScheduler(); scheduler.start()"
```

## Deployment

### Docker Deployment
```bash
# Build image
docker build -t pimp:latest .

# Push to registry
docker tag pimp:latest your-registry/pimp:latest
docker push your-registry/pimp:latest
```

### Production Deployment
```bash
# With Docker Compose
docker-compose -f docker-compose.yml up -d

# Check logs
docker-compose logs -f backend
```

## Monitoring

- **Application Logs**: `/app/logs/pimp.log`
- **Sentry**: Real-time error tracking
- **Prometheus**: Metrics collection (optional)
- **Health Check**: `/health` endpoint

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -am 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

MIT License - See LICENSE file

## Support

For issues and questions:
- GitHub Issues: https://github.com/aabc25891-ops/Pimp/issues
- Email: pimp-support@example.com

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard (React)
- [ ] Webhook notifications
- [ ] Custom alerts
- [ ] User authentication
- [ ] Multi-language support
- [ ] International e-commerce support

## Acknowledgments

- FastAPI & Uvicorn
- SQLAlchemy
- Scikit-learn & TensorFlow
- Prophet forecasting
- HuggingFace Transformers

---

**PIMP v1.0.0** - Powering Product Trends
