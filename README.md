# PIMP - Predictive Intelligence Market Platform

AI-powered product trend prediction for e-commerce sellers on Meesho, Amazon, and Flipkart.

## 🎯 Overview

PIMP predicts which products will trend **before they become popular** by analyzing:
- Google Trends data
- Reddit discussions
- Marketplace catalogs (Meesho, Amazon, Flipkart)
- Social signals (YouTube, Instagram)
- Real-time market data

## 📊 Features

- **Daily Analysis:** Runs every day at 2 AM IST automatically
- **2 Categories:** Fashion & Home Goods
- **3 Marketplaces:** Meesho, Amazon India, Flipkart
- **Prediction Output:**
  - Trend Score (0-100)
  - Probability of trending (%)
  - Confidence level
  - Detailed reasons
  - Historical trend graphs

## 🏗️ Architecture

```
Data Collection (Daily)
    ↓
ETL Pipeline (Clean & Normalize)
    ↓
ML Models (Forecasting + NLP)
    ↓
Ensemble Model (Combine signals)
    ↓
API (Serve predictions)
    ↓
Dashboard (Display results)
```

## 📁 Project Structure

```
PIMP/
├── data_collection/          # Scrapers & data fetchers
│   ├── scrapers/
│   │   ├── meesho_scraper.py
│   │   ├── amazon_scraper.py
│   │   ├── flipkart_scraper.py
│   │   └── social_scraper.py
│   ├── apis/
│   │   ├── google_trends.py
│   │   ├── reddit_api.py
│   │   └── youtube_api.py
│   └── etl_pipeline.py
├── database/
│   ├── schema.sql
│   ├── models.py
│   └── migrations/
├── ml_models/
│   ├── forecasting.py        # Time-series models
│   ├── nlp_sentiment.py       # NLP analysis
│   ├── ensemble.py            # Combine models
│   └── training/
├── backend/
│   ├── app.py                 # FastAPI server
│   ├── routes/
│   │   ├── predictions.py
│   │   ├── products.py
│   │   └── analytics.py
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
├── airflow/
│   ├── dags/
│   │   └── daily_pipeline.py
│   └── config/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── config/
│   ├── settings.py
│   └── .env.example
├── tests/
├── docs/
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   └── API.md
├── requirements.txt
├── .gitignore
└── setup.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+
- Docker & Docker Compose

### Installation

1. **Clone the repo**
```bash
git clone https://github.com/aabc25891-ops/Pimp.git
cd Pimp
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up database**
```bash
createdb pimp_db
psql pimp_db < database/schema.sql
```

4. **Configure environment variables**
```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

5. **Run data collection**
```bash
python data_collection/etl_pipeline.py
```

6. **Start API server**
```bash
python backend/app.py
```

7. **Run frontend** (in new terminal)
```bash
cd frontend
npm install
npm start
```

## 📊 Data Sources

| Source | Frequency | Purpose |
|--------|-----------|---------|
| Google Trends | Daily | Search volume trends |
| Reddit API | Daily | Community sentiment & discussions |
| Meesho | Daily | Product listings & demand |
| Amazon | Daily | Best sellers & ratings |
| Flipkart | Daily | Trending products |
| YouTube/Instagram | Weekly | Video trend signals |

## 🧠 ML Pipeline

1. **Data Preprocessing:** Clean, normalize, handle missing values
2. **Feature Engineering:** Extract signals from each source
3. **Time-Series Forecasting:** Prophet model for trend prediction
4. **NLP Analysis:** Sentiment analysis on text data
5. **Ensemble Model:** Combine all signals into final probability
6. **Calibration:** Ensure output is interpretable as true probability

## 📈 Output Format

```json
{
  "product_id": "123",
  "product_name": "Oversized Anime T-Shirt",
  "category": "Fashion",
  "trend_score": 81,
  "probability": 0.81,
  "confidence": "High",
  "time_horizon": "30 days",
  "reasons": [
    "Google searches ↑ 42%",
    "Instagram mentions ↑ 38%",
    "Meesho demand ↑ 25%",
    "12 new competitor listings"
  ],
  "historical_trend": [...],
  "prediction_date": "2025-07-21",
  "next_update": "2025-07-22"
}
```

## 🔧 Configuration

See `config/.env.example` for all available options:
- API keys (Google Trends, Reddit, YouTube, Instagram)
- Database credentials
- Email notifications
- Update frequency
- Model parameters

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [ML Models Guide](docs/MODELS.md)

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## 📝 License

MIT License - See LICENSE file

## 👨‍💻 Author

Built by aabc25891-ops

## 📧 Support

For issues or questions, open a GitHub issue.

---

**Last Updated:** 2025-07-21
