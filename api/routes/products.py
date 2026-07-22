"""Product API Routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from database.models import Product
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class ProductSchema(BaseModel):
    """Product schema"""
    product_name: str
    category: str
    price: Optional[float] = None
    rating: Optional[float] = None
    reviews_count: int = 0
    source: str
    url: Optional[str] = None
    
    class Config:
        from_attributes = True


class ProductResponse(ProductSchema):
    """Product response schema"""
    id: str
    created_at: str


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    category: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all products with optional filtering"""
    try:
        query = db.query(Product).filter(Product.is_active == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        if source:
            query = query.filter(Product.source == source)
        
        products = query.offset(skip).limit(limit).all()
        return products
    
    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching products")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get product by ID"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching product")


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductSchema,
    db: Session = Depends(get_db)
):
    """Create new product"""
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        logger.info(f"Created product: {db_product.id}")
        return db_product
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating product")


@router.get("/category/{category}/trending")
async def get_trending_in_category(
    category: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get trending products in category"""
    try:
        from database.models import TrendPrediction
        from datetime import date
        
        products = db.query(Product).join(
            TrendPrediction,
            Product.id == TrendPrediction.product_id
        ).filter(
            Product.category == category,
            TrendPrediction.prediction_date == date.today(),
            TrendPrediction.trend_score >= 70
        ).order_by(
            TrendPrediction.trend_score.desc()
        ).limit(limit).all()
        
        return products
    
    except Exception as e:
        logger.error(f"Error fetching trending products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching trending products")
