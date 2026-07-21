"""
PIMP Configuration Settings
Loads environment variables and provides centralized configuration
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application Settings"""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://pimp_user:password@localhost:5432/pimp_db"
    )
    DATABASE_ECHO: bool = DEBUG
    
    # API Configuration
    FASTAPI_HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}" if REDIS_PASSWORD else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Google API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_SEARCH_ENGINE_ID: str = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    
    # Reddit API
    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "PIMP/1.0")
    
    # YouTube API
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    
    # Instagram
    INSTAGRAM_USERNAME: str = os.getenv("INSTAGRAM_USERNAME", "")
    INSTAGRAM_PASSWORD: str = os.getenv("INSTAGRAM_PASSWORD", "")
    
    # Data Collection Settings
    SCRAPE_SCHEDULE: str = os.getenv("SCRAPE_SCHEDULE", "0 2 * * *")  # 2 AM daily
    MEESHO_UPDATE_FREQUENCY: int = int(os.getenv("MEESHO_UPDATE_FREQUENCY", "24"))
    AMAZON_UPDATE_FREQUENCY: int = int(os.getenv("AMAZON_UPDATE_FREQUENCY", "24"))
    FLIPKART_UPDATE_FREQUENCY: int = int(os.getenv("FLIPKART_UPDATE_FREQUENCY", "24"))
    REDDIT_UPDATE_FREQUENCY: int = int(os.getenv("REDDIT_UPDATE_FREQUENCY", "6"))
    
    # ML Model Settings
    FORECAST_HORIZON: int = int(os.getenv("FORECAST_HORIZON", "30"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
    MIN_DATA_POINTS: int = int(os.getenv("MIN_DATA_POINTS", "30"))
    
    # Categories
    CATEGORIES: List[str] = os.getenv("CATEGORIES", "Fashion,Home Goods").split(",")
    
    # Email Notifications
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    NOTIFICATION_EMAIL: str = os.getenv("NOTIFICATION_EMAIL", "")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/pimp.log")
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "")
    
    # Sentry
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    
    # Scraper Settings
    SCRAPER_DELAY: float = float(os.getenv("SCRAPER_DELAY", "2"))
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "100"))
    USE_PROXY: bool = os.getenv("USE_PROXY", "False").lower() == "true"
    PROXY_LIST: List[str] = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []


# Create global settings instance
settings = Settings()
