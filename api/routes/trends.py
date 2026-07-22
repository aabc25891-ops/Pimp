"""Trends API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import GoogleTrendsData, RedditData, TrendPrediction
from datetime import datetime, timedelta, date
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/google/trending")
async def get_google_trending(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get trending Google searches"""
    try:
        cutoff_date = date.today() - timedelta(days=days)
        
        trends = db.query(GoogleTrendsData).filter(
            GoogleTrendsData.date >= cutoff_date,
            GoogleTrendsData.region == 'IN'
        ).order_by(
            GoogleTrendsData.trend_value.desc()
        ).limit(limit).all()
        
        return trends
    
    except Exception as e:
        logger.error(f"Error fetching Google trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching Google trends")


@router.get("/reddit/trending")
async def get_reddit_trending(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get trending Reddit posts"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        posts = db.query(RedditData).filter(
            RedditData.date >= cutoff_date
        ).order_by(
            RedditData.upvotes.desc()
        ).limit(limit).all()
        
        return posts
    
    except Exception as e:
        logger.error(f"Error fetching Reddit trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching Reddit trends")


@router.get("/keyword/{keyword}")
async def get_keyword_trend(
    keyword: str,
    db: Session = Depends(get_db)
):
    """Get trend data for specific keyword"""
    try:
        google_data = db.query(GoogleTrendsData).filter(
            GoogleTrendsData.keyword.ilike(f"%{keyword}%")
        ).order_by(
            GoogleTrendsData.date.desc()
        ).limit(100).all()
        
        reddit_data = db.query(RedditData).filter(
            RedditData.keywords.icontains([keyword])
        ).order_by(
            RedditData.date.desc()
        ).limit(50).all()
        
        return {
            "keyword": keyword,
            "google_trends": google_data,
            "reddit_mentions": reddit_data,
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        logger.error(f"Error fetching keyword trend: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching keyword trend")


@router.get("/momentum")
async def get_trend_momentum(
    category: str = Query(None),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get trend momentum (acceleration of trends)"""
    try:
        from sqlalchemy import func
        
        cutoff_date = date.today() - timedelta(days=days)
        
        query = db.query(
            TrendPrediction.product_id,
            func.count(TrendPrediction.id).label('prediction_count'),
            func.avg(TrendPrediction.trend_score).label('avg_trend_score'),
            func.max(TrendPrediction.trend_score).label('max_trend_score')
        ).filter(
            TrendPrediction.prediction_date >= cutoff_date
        )
        
        if category:
            from database.models import Product
            query = query.join(Product).filter(Product.category == category)
        
        momentum = query.group_by(
            TrendPrediction.product_id
        ).order_by(
            func.max(TrendPrediction.trend_score).desc()
        ).limit(50).all()
        
        return momentum
    
    except Exception as e:
        logger.error(f"Error calculating trend momentum: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating trend momentum")
