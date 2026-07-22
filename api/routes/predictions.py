"""Prediction API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from database.models import Product, TrendPrediction, TrendReason
from pydantic import BaseModel
from datetime import date
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class PredictionSchema(BaseModel):
    """Prediction schema"""
    product_id: str
    trend_score: float
    probability: float
    confidence: str
    
    class Config:
        from_attributes = True


class PredictionResponse(PredictionSchema):
    """Prediction response schema"""
    id: str
    prediction_date: date
    created_at: str


class TrendReasonSchema(BaseModel):
    """Trend reason schema"""
    reason: str
    signal_type: str
    signal_strength: float


@router.get("/", response_model=List[PredictionResponse])
async def list_predictions(
    product_id: Optional[str] = Query(None),
    min_score: float = Query(0, ge=0, le=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List predictions"""
    try:
        query = db.query(TrendPrediction).filter(
            TrendPrediction.trend_score >= min_score
        )
        
        if product_id:
            query = query.filter(TrendPrediction.product_id == product_id)
        
        predictions = query.offset(skip).limit(limit).all()
        return predictions
    
    except Exception as e:
        logger.error(f"Error listing predictions: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching predictions")


@router.get("/product/{product_id}")
async def get_product_predictions(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get predictions for a specific product"""
    try:
        # Check if product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        predictions = db.query(TrendPrediction).filter(
            TrendPrediction.product_id == product_id
        ).order_by(TrendPrediction.prediction_date.desc()).all()
        
        return {
            "product_id": product_id,
            "product_name": product.product_name,
            "predictions": predictions
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product predictions: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching predictions")


@router.get("/top-trending")
async def get_top_trending(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top trending products"""
    try:
        predictions = db.query(TrendPrediction).join(
            Product,
            TrendPrediction.product_id == Product.id
        ).filter(
            TrendPrediction.prediction_date == date.today()
        ).order_by(
            TrendPrediction.trend_score.desc()
        ).limit(limit).all()
        
        return predictions
    
    except Exception as e:
        logger.error(f"Error fetching top trending: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching trending products")


@router.post("/", response_model=PredictionResponse)
async def create_prediction(
    prediction: PredictionSchema,
    db: Session = Depends(get_db)
):
    """Create new prediction"""
    try:
        db_prediction = TrendPrediction(
            **prediction.dict(),
            prediction_date=date.today()
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        logger.info(f"Created prediction for product: {prediction.product_id}")
        return db_prediction
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating prediction")
