"""Analytics API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import TrendPrediction, Product, ModelMetrics, ApiLog
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """Get overall analytics summary"""
    try:
        total_products = db.query(Product).filter(Product.is_active == True).count()
        total_predictions = db.query(TrendPrediction).count()
        
        # Get average trend score
        avg_trend = db.query(
            func.avg(TrendPrediction.trend_score)
        ).scalar() or 0
        
        # High confidence predictions
        high_confidence = db.query(TrendPrediction).filter(
            TrendPrediction.confidence == 'High'
        ).count()
        
        return {
            "total_products": total_products,
            "total_predictions": total_predictions,
            "average_trend_score": float(avg_trend),
            "high_confidence_predictions": high_confidence,
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching analytics")


@router.get("/category-stats")
async def get_category_statistics(db: Session = Depends(get_db)):
    """Get statistics by category"""
    try:
        from sqlalchemy import func
        
        categories = db.query(
            Product.category,
            func.count(Product.id).label('product_count'),
            func.avg(Product.rating).label('avg_rating'),
            func.avg(Product.price).label('avg_price')
        ).group_by(Product.category).all()
        
        stats = []
        for cat, count, rating, price in categories:
            stats.append({
                "category": cat,
                "product_count": count,
                "average_rating": float(rating) if rating else 0,
                "average_price": float(price) if price else 0
            })
        
        return stats
    
    except Exception as e:
        logger.error(f"Error getting category stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching category statistics")


@router.get("/model-performance")
async def get_model_performance(db: Session = Depends(get_db)):
    """Get model performance metrics"""
    try:
        metrics = db.query(ModelMetrics).order_by(
            ModelMetrics.created_at.desc()
        ).limit(100).all()
        
        performance = {}
        for metric in metrics:
            if metric.model_type not in performance:
                performance[metric.model_type] = {}
            
            performance[metric.model_type][metric.metric_name] = metric.metric_value
        
        return performance
    
    except Exception as e:
        logger.error(f"Error getting model performance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching model performance")


@router.get("/api-usage")
async def get_api_usage_stats(
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    """Get API usage statistics"""
    try:
        from sqlalchemy import func
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        stats = db.query(
            ApiLog.endpoint,
            ApiLog.method,
            func.count(ApiLog.id).label('call_count'),
            func.avg(ApiLog.response_time).label('avg_response_time')
        ).filter(
            ApiLog.created_at >= cutoff_time
        ).group_by(
            ApiLog.endpoint,
            ApiLog.method
        ).all()
        
        result = []
        for endpoint, method, count, avg_time in stats:
            result.append({
                "endpoint": endpoint,
                "method": method,
                "call_count": count,
                "average_response_time_ms": float(avg_time) if avg_time else 0
            })
        
        return result
    
    except Exception as e:
        logger.error(f"Error getting API usage stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching API usage statistics")
