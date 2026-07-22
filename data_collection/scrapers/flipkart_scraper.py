"""Flipkart Product Scraper"""

import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class FlipkartScraper:
    """Scrapes product data from Flipkart"""
    
    BASE_URL = "https://www.flipkart.com/search"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-IN,en;q=0.9'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def scrape_search_results(self, query: str, page: int = 1) -> List[Dict]:
        """
        Scrape search results from Flipkart
        
        Args:
            query: Search query
            page: Page number
        
        Returns:
            List of product dictionaries
        """
        try:
            params = {
                'q': query,
                'page': page
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            items = soup.find_all('div', {'class': '_2kHmtP'})
            
            for item in items:
                try:
                    title_elem = item.find('a', {'class': 'IRpwTa'})
                    price_elem = item.find('div', {'class': '_30jeq3 _1_WHN1'})
                    rating_elem = item.find('div', {'class': '_3LWZlK'})
                    
                    if not title_elem:
                        continue
                    
                    product = {
                        'product_name': title_elem.get_text(strip=True),
                        'category': query,
                        'price': float(price_elem.get_text(strip=True).replace('₹', '').replace(',', '')) if price_elem else 0,
                        'rating': float(rating_elem.get_text(strip=True)) if rating_elem else 0,
                        'reviews_count': 0,
                        'seller_name': 'Flipkart',
                        'source': 'flipkart',
                        'source_id': title_elem.get('href', '').split('/p/')[-1].split('?')[0] if title_elem else None,
                        'url': f"https://www.flipkart.com{title_elem.get('href', '')}" if title_elem else '',
                        'description': title_elem.get_text(strip=True)
                    }
                    products.append(product)
                except Exception as e:
                    logger.warning(f"Error parsing Flipkart product: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(products)} products from Flipkart for query: {query}")
            time.sleep(settings.SCRAPER_DELAY)
            return products
            
        except Exception as e:
            logger.error(f"Error scraping Flipkart: {str(e)}")
            return []
