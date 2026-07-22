"""Airflow DAG for PIMP Data Pipeline"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Define DAG
default_args = {
    'owner': 'pimp',
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['pimp-alerts@example.com']
}

dag = DAG(
    'pimp_data_pipeline',
    default_args=default_args,
    description='PIMP Product Trend Prediction Pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    tags=['pimp', 'prediction']
)


def scrape_meesho():
    """Scrape Meesho products"""
    try:
        from data_collection.scrapers.meesho_scraper import MeeshoScraper
        from database.database import SessionLocal
        from database.models import Product
        
        scraper = MeeshoScraper()
        products = scraper.scrape_all_categories()
        
        db = SessionLocal()
        for product in products:
            # Check if product exists
            existing = db.query(Product).filter(
                Product.source_id == product.get('source_id')
            ).first()
            
            if not existing:
                db_product = Product(**product)
                db.add(db_product)
        
        db.commit()
        db.close()
        logger.info(f"Scraped {len(products)} products from Meesho")
    
    except Exception as e:
        logger.error(f"Error scraping Meesho: {str(e)}")
        raise


def scrape_amazon():
    """Scrape Amazon products"""
    try:
        from data_collection.scrapers.amazon_scraper import AmazonScraper
        from database.database import SessionLocal
        from database.models import Product
        from config.settings import settings
        
        scraper = AmazonScraper()
        all_products = []
        
        for category in settings.CATEGORIES:
            products = scraper.scrape_bestsellers(category)
            all_products.extend(products)
        
        db = SessionLocal()
        for product in all_products:
            existing = db.query(Product).filter(
                Product.source_id == product.get('source_id')
            ).first()
            
            if not existing:
                db_product = Product(**product)
                db.add(db_product)
        
        db.commit()
        db.close()
        logger.info(f"Scraped {len(all_products)} products from Amazon")
    
    except Exception as e:
        logger.error(f"Error scraping Amazon: {str(e)}")
        raise


def scrape_flipkart():
    """Scrape Flipkart products"""
    try:
        from data_collection.scrapers.flipkart_scraper import FlipkartScraper
        from database.database import SessionLocal
        from database.models import Product
        from config.settings import settings
        
        scraper = FlipkartScraper()
        all_products = []
        
        for category in settings.CATEGORIES:
            products = scraper.scrape_search_results(category)
            all_products.extend(products)
        
        db = SessionLocal()
        for product in all_products:
            existing = db.query(Product).filter(
                Product.source_id == product.get('source_id')
            ).first()
            
            if not existing:
                db_product = Product(**product)
                db.add(db_product)
        
        db.commit()
        db.close()
        logger.info(f"Scraped {len(all_products)} products from Flipkart")
    
    except Exception as e:
        logger.error(f"Error scraping Flipkart: {str(e)}")
        raise


def collect_reddit_data():
    """Collect Reddit data"""
    try:
        from data_collection.apis.reddit_api import RedditCollector
        from database.database import SessionLocal
        from database.models import RedditData
        from config.settings import settings
        
        collector = RedditCollector()
        posts = collector.collect_posts(settings.CATEGORIES)
        
        db = SessionLocal()
        for post in posts:
            existing = db.query(RedditData).filter(
                RedditData.post_id == post.get('post_id')
            ).first()
            
            if not existing:
                db_post = RedditData(**post)
                db.add(db_post)
        
        db.commit()
        db.close()
        logger.info(f"Collected {len(posts)} Reddit posts")
    
    except Exception as e:
        logger.error(f"Error collecting Reddit data: {str(e)}")
        raise


def collect_google_trends():
    """Collect Google Trends data"""
    try:
        from data_collection.apis.google_trends import GoogleTrendsCollector
        from database.database import SessionLocal
        from database.models import GoogleTrendsData
        from config.settings import settings
        from datetime import date
        
        collector = GoogleTrendsCollector()
        trending = collector.get_trending_keywords(settings.CATEGORIES)
        
        db = SessionLocal()
        for keyword in settings.CATEGORIES:
            rising = collector.get_rising_searches()
            
            for item in rising:
                existing = db.query(GoogleTrendsData).filter(
                    GoogleTrendsData.keyword == item['query'],
                    GoogleTrendsData.date == date.today()
                ).first()
                
                if not existing:
                    db_trend = GoogleTrendsData(
                        keyword=item['query'],
                        trend_value=50,
                        region='IN',
                        date=date.today()
                    )
                    db.add(db_trend)
        
        db.commit()
        db.close()
        logger.info("Collected Google Trends data")
    
    except Exception as e:
        logger.error(f"Error collecting Google Trends: {str(e)}")
        raise


def generate_predictions():
    """Generate trend predictions"""
    try:
        from database.database import SessionLocal
        from database.models import Product, TrendPrediction, HistoricalData
        from ml_models.ensemble import EnsemblePredictor
        from ml_models.feature_engineering import FeatureEngineer
        import pandas as pd
        import numpy as np
        from datetime import date
        
        db = SessionLocal()
        products = db.query(Product).filter(Product.is_active == True).all()
        
        predictor = EnsemblePredictor()
        predictor.build_base_models()
        
        for product in products:
            # Get historical data
            historical = db.query(HistoricalData).filter(
                HistoricalData.product_id == product.id
            ).order_by(HistoricalData.time.desc()).limit(100).all()
            
            if len(historical) < 30:
                continue
            
            # Prepare features
            df = pd.DataFrame([
                {
                    'time': h.time,
                    'value': float(h.metric_value)
                } for h in historical
            ])
            
            # Generate prediction
            X = df[['value']].values
            y = df['value'].values
            
            try:
                predictor.train_base_models(X, y)
                prediction, _ = predictor.predict_ensemble(X[-1:].reshape(1, -1))
                
                trend_score = float(prediction[0])
                confidence = 'High' if trend_score > 70 else 'Medium' if trend_score > 40 else 'Low'
                
                # Save prediction
                db_pred = TrendPrediction(
                    product_id=product.id,
                    trend_score=trend_score,
                    probability=0.85,
                    confidence=confidence,
                    prediction_date=date.today()
                )
                db.add(db_pred)
            except:
                continue
        
        db.commit()
        db.close()
        logger.info("Generated predictions for products")
    
    except Exception as e:
        logger.error(f"Error generating predictions: {str(e)}")
        raise


# Define tasks
task_scrape_meesho = PythonOperator(
    task_id='scrape_meesho',
    python_callable=scrape_meesho,
    dag=dag
)

task_scrape_amazon = PythonOperator(
    task_id='scrape_amazon',
    python_callable=scrape_amazon,
    dag=dag
)

task_scrape_flipkart = PythonOperator(
    task_id='scrape_flipkart',
    python_callable=scrape_flipkart,
    dag=dag
)

task_reddit = PythonOperator(
    task_id='collect_reddit',
    python_callable=collect_reddit_data,
    dag=dag
)

task_google_trends = PythonOperator(
    task_id='collect_google_trends',
    python_callable=collect_google_trends,
    dag=dag
)

task_predictions = PythonOperator(
    task_id='generate_predictions',
    python_callable=generate_predictions,
    dag=dag
)

# Define dependencies
[task_scrape_meesho, task_scrape_amazon, task_scrape_flipkart, task_reddit, task_google_trends] >> task_predictions
