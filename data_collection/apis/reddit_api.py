"""Reddit Data Collection"""

import praw
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from config.settings import settings

logger = logging.getLogger(__name__)


class RedditCollector:
    """Collects data from Reddit using PRAW API"""
    
    SUBREDDITS = [
        'r/fashion',
        'r/HomeImprovement',
        'r/InteriorDesign',
        'r/Ecommerce',
        'r/ShoppingDeals'
    ]
    
    def __init__(self):
        """Initialize Reddit API client"""
        try:
            self.reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT
            )
        except Exception as e:
            logger.error(f"Error initializing Reddit API: {str(e)}")
            self.reddit = None
    
    def collect_posts(self, keywords: List[str], time_filter: str = 'day') -> List[Dict]:
        """
        Collect Reddit posts matching keywords
        
        Args:
            keywords: List of keywords to search
            time_filter: Time filter ('day', 'week', 'month')
        
        Returns:
            List of post dictionaries
        """
        if not self.reddit:
            return []
        
        posts = []
        
        try:
            for keyword in keywords:
                try:
                    # Search posts
                    search_results = self.reddit.subreddit('all').search(
                        keyword,
                        time_filter=time_filter,
                        limit=100
                    )
                    
                    for post in search_results:
                        post_data = {
                            'subreddit': post.subreddit.display_name,
                            'post_id': post.id,
                            'title': post.title,
                            'content': post.selftext,
                            'upvotes': post.score,
                            'comments_count': post.num_comments,
                            'date': datetime.fromtimestamp(post.created_utc),
                            'url': post.url,
                            'keywords': keyword
                        }
                        posts.append(post_data)
                    
                    logger.info(f"Collected {len(search_results)} posts for keyword: {keyword}")
                
                except Exception as e:
                    logger.warning(f"Error collecting Reddit posts for {keyword}: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in Reddit collection: {str(e)}")
        
        return posts
    
    def get_trending_topics(self, subreddit: str = 'Trending') -> List[Dict]:
        """Get trending topics from Reddit"""
        if not self.reddit:
            return []
        
        try:
            trending_posts = self.reddit.subreddit(subreddit).hot(limit=50)
            topics = []
            
            for post in trending_posts:
                topic = {
                    'title': post.title,
                    'upvotes': post.score,
                    'comments': post.num_comments,
                    'created_at': datetime.fromtimestamp(post.created_utc)
                }
                topics.append(topic)
            
            return topics
        
        except Exception as e:
            logger.error(f"Error getting Reddit trending topics: {str(e)}")
            return []
