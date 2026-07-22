"""Utilities and helper functions"""

import logging
from typing import Dict, List, Any
import json
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def clean_product_data(product: Dict) -> Dict:
        """
        Clean product data
        
        Args:
            product: Product dictionary
        
        Returns:
            Cleaned product dictionary
        """
        try:
            cleaned = {
                'product_name': str(product.get('product_name', '')).strip(),
                'category': str(product.get('category', '')).strip(),
                'price': float(product.get('price', 0)) if product.get('price') else 0,
                'rating': float(product.get('rating', 0)) if product.get('rating') else 0,
                'reviews_count': int(product.get('reviews_count', 0)),
                'source': str(product.get('source', '')).strip(),
                'source_id': str(product.get('source_id', '')).strip(),
                'url': str(product.get('url', '')).strip(),
                'description': str(product.get('description', '')).strip()
            }
            return cleaned
        except Exception as e:
            logger.error(f"Error cleaning product data: {str(e)}")
            return {}
    
    @staticmethod
    def normalize_price(price: float, min_price: float, max_price: float) -> float:
        """
        Normalize price to 0-1 range
        
        Args:
            price: Price value
            min_price: Minimum price
            max_price: Maximum price
        
        Returns:
            Normalized price
        """
        if max_price == min_price:
            return 0.5
        return (price - min_price) / (max_price - min_price)
    
    @staticmethod
    def calculate_trend_score(metrics: Dict) -> float:
        """
        Calculate trend score from metrics
        
        Args:
            metrics: Dictionary with metrics
        
        Returns:
            Trend score (0-100)
        """
        try:
            search_volume = float(metrics.get('search_volume', 0))
            reddit_mentions = float(metrics.get('reddit_mentions', 0))
            social_engagement = float(metrics.get('social_engagement', 0))
            sentiment = float(metrics.get('sentiment', 0))
            
            score = (search_volume * 0.3 + 
                    reddit_mentions * 0.25 + 
                    social_engagement * 0.25 + 
                    sentiment * 0.2)
            
            return min(100, max(0, score))
        
        except Exception as e:
            logger.error(f"Error calculating trend score: {str(e)}")
            return 0.0


class CacheManager:
    """Cache management utilities"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get(self, key: str) -> Any:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set cache value
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live (seconds)
        """
        try:
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")
    
    def delete(self, key: str):
        """
        Delete cache key
        
        Args:
            key: Cache key
        """
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Error deleting cache: {str(e)}")
    
    def clear_pattern(self, pattern: str):
        """
        Clear cache by pattern
        
        Args:
            pattern: Redis pattern
        """
        try:
            keys = self.redis.keys(pattern)
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Error clearing cache pattern: {str(e)}")


class TextProcessor:
    """Text processing utilities"""
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            min_length: Minimum keyword length
        
        Returns:
            List of keywords
        """
        try:
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize
            import nltk
            
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
            
            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            keywords = [
                word for word in tokens
                if word.isalnum() and len(word) >= min_length and word not in stop_words
            ]
            
            return list(set(keywords))
        
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    @staticmethod
    def generate_hash(text: str) -> str:
        """
        Generate hash of text
        
        Args:
            text: Input text
        
        Returns:
            SHA256 hash
        """
        return hashlib.sha256(text.encode()).hexdigest()
