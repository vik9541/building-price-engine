"""Prices API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, CompetitorPrice
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{product_id}")
async def get_product_prices(product_id: int, db: Session = Depends(get_db)):
    """Get price history for a product."""
    prices = db.query(CompetitorPrice).filter(
        CompetitorPrice.product_id == product_id
    ).order_by(CompetitorPrice.created_at.desc()).all()
    return prices


@router.get("/compare/{product_id}")
async def compare_prices(product_id: int, db: Session = Depends(get_db)):
    """Compare prices with competitors."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"error": "Product not found"}
    
    competitor_prices = db.query(CompetitorPrice).filter(
        CompetitorPrice.product_id == product_id
    ).all()
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "our_price": product.our_price,
        "competitor_prices": [
            {
                "competitor": cp.competitor.name,
                "price": cp.price,
                "url": cp.competitor_url,
                "in_stock": cp.in_stock,
            }
            for cp in competitor_prices
        ]
    }
