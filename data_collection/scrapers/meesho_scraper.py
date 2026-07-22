"""Meesho Product Scraper"""

import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class MeeshoScraper:
    """Scrapes product data from Meesho marketplace"""
    
    BASE_URL = "https://www.meesho.com/api/v1/products"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def scrape_category(self, category: str, page: int = 1) -> List[Dict]:
        """
        Scrape products from a specific category
        
        Args:
            category: Category name (e.g., 'Fashion', 'Home Goods')
            page: Page number
        
        Returns:
            List of product dictionaries
        """
        try:
            params = {
                'search': category,
                'page': page,
                'limit': 50
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            products = []
            
            for item in data.get('products', []):
                product = {
                    'product_name': item.get('title', 'Unknown'),
                    'category': category,
                    'price': float(item.get('price', 0)),
                    'rating': float(item.get('rating', 0)),
                    'reviews_count': int(item.get('rating_count', 0)),
                    'seller_name': item.get('seller_name', 'Unknown'),
                    'source': 'meesho',
                    'source_id': item.get('product_id'),
                    'url': item.get('url'),
                    'description': item.get('description', '')
                }
                products.append(product)
            
            logger.info(f"Scraped {len(products)} products from Meesho category: {category}")
            time.sleep(settings.SCRAPER_DELAY)
            return products
            
        except Exception as e:
            logger.error(f"Error scraping Meesho: {str(e)}")
            return []
    
    def scrape_all_categories(self) -> List[Dict]:
        """Scrape all categories"""
        all_products = []
        
        for category in settings.CATEGORIES:
            products = self.scrape_category(category)
            all_products.extend(products)
        
        return all_products
