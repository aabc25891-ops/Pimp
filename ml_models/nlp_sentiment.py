"""NLP-based Sentiment Analysis"""

import pandas as pd
import numpy as np
from transformers import pipeline
from typing import Dict, List, Tuple
import logging
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')


class SentimentAnalyzer:
    """NLP-based sentiment analysis for trend detection"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize sentiment analyzer
        
        Args:
            model_name: HuggingFace model name
        """
        try:
            self.sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
            self.sia = SentimentIntensityAnalyzer()
            logger.info("Sentiment analyzer initialized")
        except Exception as e:
            logger.warning(f"Error loading transformer model: {str(e)}")
            self.sentiment_pipeline = None
            self.sia = SentimentIntensityAnalyzer()
    
    def analyze_sentiment_transformers(self, text: str) -> Dict:
        """
        Analyze sentiment using transformer model
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment score
        """
        if not self.sentiment_pipeline or not text or len(str(text).strip()) == 0:
            return {'label': 'NEUTRAL', 'score': 0.0}
        
        try:
            # Truncate long texts
            text = str(text)[:512]
            result = self.sentiment_pipeline(text)[0]
            
            # Convert to normalized score -1 to 1
            score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
            
            return {
                'label': result['label'],
                'score': score,
                'confidence': result['score']
            }
        
        except Exception as e:
            logger.warning(f"Error in transformer sentiment analysis: {str(e)}")
            return {'label': 'NEUTRAL', 'score': 0.0}
    
    def analyze_sentiment_vader(self, text: str) -> Dict:
        """
        Analyze sentiment using VADER
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            if not text or len(str(text).strip()) == 0:
                return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
            
            scores = self.sia.polarity_scores(str(text))
            return scores
        
        except Exception as e:
            logger.warning(f"Error in VADER sentiment analysis: {str(e)}")
            return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
    
    def extract_keywords(self, texts: List[str], top_n: int = 10) -> List[str]:
        """
        Extract keywords from texts using TF-IDF
        
        Args:
            texts: List of texts
            top_n: Number of top keywords
        
        Returns:
            List of keywords
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            keywords = vectorizer.get_feature_names_out().tolist()
            return keywords
        
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def analyze_batch(self, texts: List[str], method: str = 'vader') -> List[Dict]:
        """
        Analyze sentiment for batch of texts
        
        Args:
            texts: List of texts
            method: 'vader' or 'transformers'
        
        Returns:
            List of sentiment dictionaries
        """
        results = []
        
        for text in texts:
            if method == 'transformers':
                result = self.analyze_sentiment_transformers(text)
            else:
                result = self.analyze_sentiment_vader(text)
            
            results.append(result)
        
        return results
    
    def calculate_sentiment_score(self, df: pd.DataFrame, text_col: str) -> pd.Series:
        """
        Calculate sentiment scores for DataFrame column
        
        Args:
            df: Input DataFrame
            text_col: Text column name
        
        Returns:
            Series with sentiment scores
        """
        sentiment_scores = []
        
        for text in df[text_col]:
            scores = self.analyze_sentiment_vader(text)
            sentiment_scores.append(scores['compound'])
        
        return pd.Series(sentiment_scores)
