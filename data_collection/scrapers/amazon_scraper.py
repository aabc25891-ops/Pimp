"""Amazon India Product Scraper"""

import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AmazonScraper:
    """Scrapes product data from Amazon India"""
    
    BASE_URL = "https://www.amazon.in/s"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-IN,en;q=0.9'
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def scrape_search_results(self, query: str, page: int = 1) -> List[Dict]:
        """
        Scrape search results from Amazon
        
        Args:
            query: Search query
            page: Page number
        
        Returns:
            List of product dictionaries
        """
        try:
            params = {
                'k': query,
                'page': page
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            items = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for item in items:
                try:
                    title_elem = item.find('h2', class_='s-line-clamp-2')
                    price_elem = item.find('span', class_='a-price-whole')
                    rating_elem = item.find('span', class_='a-icon-star-small')
                    link_elem = item.find('a', class_='s-no-outline')
                    
                    if not title_elem:
                        continue
                    
                    product = {
                        'product_name': title_elem.get_text(strip=True),
                        'category': query,
                        'price': float(price_elem.get_text(strip=True).replace('₹', '').replace(',', '')) if price_elem else 0,
                        'rating': float(rating_elem.get_text(strip=True).split()[0]) if rating_elem else 0,
                        'reviews_count': 0,
                        'seller_name': 'Amazon India',
                        'source': 'amazon',
                        'source_id': link_elem.get('href', '').split('/dp/')[-1].split('/')[0] if link_elem else None,
                        'url': f"https://www.amazon.in{link_elem.get('href', '')}" if link_elem else '',
                        'description': title_elem.get_text(strip=True)
                    }
                    products.append(product)
                except Exception as e:
                    logger.warning(f"Error parsing Amazon product: {str(e)}")
                    continue
            
            logger.info(f"Scraped {len(products)} products from Amazon for query: {query}")
            time.sleep(settings.SCRAPER_DELAY)
            return products
            
        except Exception as e:
            logger.error(f"Error scraping Amazon: {str(e)}")
            return []
    
    def scrape_bestsellers(self, category: str) -> List[Dict]:
        """Scrape bestsellers from category"""
        return self.scrape_search_results(category)
