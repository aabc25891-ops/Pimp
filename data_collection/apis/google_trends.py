"""Google Trends Data Collection"""

from pytrends.request import TrendReq
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from config.settings import settings

logger = logging.getLogger(__name__)


class GoogleTrendsCollector:
    """Collects data from Google Trends"""
    
    def __init__(self):
        """Initialize Google Trends client"""
        self.pytrends = TrendReq(hl='en-IN', tz=330)  # India timezone
    
    def get_trending_keywords(self, keywords: List[str], timeframe: str = 'today 1-m') -> Dict:
        """
        Get trend data for keywords
        
        Args:
            keywords: List of keywords (max 5)
            timeframe: Time period ('today 1-m', 'today 3-m', etc.)
        
        Returns:
            Dictionary with trend data
        """
        try:
            if len(keywords) > 5:
                keywords = keywords[:5]
            
            self.pytrends.build_payload(
                kw_list=keywords,
                timeframe=timeframe,
                geo='IN'  # India
            )
            
            interest_over_time = self.pytrends.interest_over_time()
            suggestions = self.pytrends.suggestions()
            
            return {
                'interest_over_time': interest_over_time,
                'suggestions': suggestions
            }
        
        except Exception as e:
            logger.error(f"Error getting Google Trends data: {str(e)}")
            return {}
    
    def get_rising_searches(self, geo: str = 'IN', category: int = 0) -> List[Dict]:
        """
        Get rising search queries
        
        Args:
            geo: Geographic location code
            category: Category ID
        
        Returns:
            List of rising search queries
        """
        try:
            rising_searches = self.pytrends.trending_searches(pn=geo)
            
            result = []
            for query in rising_searches.values:
                result.append({
                    'query': query[0],
                    'geo': geo,
                    'trend_type': 'rising'
                })
            
            return result
        
        except Exception as e:
            logger.error(f"Error getting rising searches: {str(e)}")
            return []
    
    def get_top_searches(self, geo: str = 'IN', category: int = 0) -> List[Dict]:
        """
        Get top search queries
        
        Args:
            geo: Geographic location code
            category: Category ID
        
        Returns:
            List of top search queries
        """
        try:
            top_searches = self.pytrends.top_searches(pn=geo)
            
            result = []
            for query in top_searches.values:
                result.append({
                    'query': query[0],
                    'geo': geo,
                    'trend_type': 'top'
                })
            
            return result
        
        except Exception as e:
            logger.error(f"Error getting top searches: {str(e)}")
            return []
