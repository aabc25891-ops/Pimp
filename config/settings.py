"""Configuration settings for PIMP"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "PIMP"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # FastAPI
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://pimp:pimp_secure_pwd@localhost:5432/pimp_db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_EXPIRE_TIME: int = 3600
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/pimp.log"
    
    # External APIs
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USER_AGENT: str = "PIMP/1.0 (by aabc25891-ops)"
    REDDIT_UPDATE_FREQUENCY: int = 6  # hours
    
    # E-commerce Scrapers
    AMAZON_UPDATE_FREQUENCY: int = 24  # hours
    FLIPKART_UPDATE_FREQUENCY: int = 24  # hours
    MEESHO_UPDATE_FREQUENCY: int = 24  # hours
    
    # Categories to track
    CATEGORIES: List[str] = [
        "Electronics",
        "Fashion",
        "Home & Kitchen",
        "Sports",
        "Beauty",
        "Books",
        "Toys & Games"
    ]
    
    # ML Settings
    ML_MODEL_PATH: str = "models/"
    ML_BATCH_SIZE: int = 32
    ML_EPOCHS: int = 10
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get settings instance"""
    return Settings()


settings = get_settings()
