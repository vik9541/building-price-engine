"""Price monitoring API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models_extended import (
    PriceSource, MarketAnalysis, CompetitorPriceRanking, 
    PriceAlert, ProductSourceMapping
)
from app import schemas
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/price-sources/", tags=["Monitoring"])
async def list_price_sources(db: Session = Depends(get_db)):
    """List all price sources."""
    sources = db.query(PriceSource).all()
    return sources


@router.get("/market-analysis/{product_id}", tags=["Monitoring"])
async def get_market_analysis(product_id: int, db: Session = Depends(get_db)):
    """Get market analysis for product."""
    analysis = db.query(MarketAnalysis).filter(
        MarketAnalysis.product_id == product_id
    ).order_by(MarketAnalysis.analysis_date.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found")
    
    return {
        "product_id": product_id,
        "analysis": analysis,
        "market_data": {
            "min_price": analysis.price_min,
            "max_price": analysis.price_max,
            "avg_price": analysis.price_avg,
            "our_position": analysis.our_position,
            "sellers_count": analysis.active_sellers_count,
        },
        "trends": {
            "24h": analysis.price_trend_24h,
            "7d": analysis.price_trend_7d,
            "30d": analysis.price_trend_30d,
        }
    }


@router.get("/price-ranking/{product_id}", tags=["Monitoring"])
async def get_price_ranking(product_id: int, db: Session = Depends(get_db)):
    """Get price ranking for product."""
    ranking = db.query(CompetitorPriceRanking).filter(
        CompetitorPriceRanking.product_id == product_id
    ).order_by(CompetitorPriceRanking.analysis_date.desc()).first()
    
    if not ranking:
        raise HTTPException(status_code=404, detail="No ranking found")
    
    return {
        "product_id": product_id,
        "our_rank": ranking.our_rank,
        "total_competitors": ranking.total_competitors,
        "recommended_price": ranking.recommended_price,
        "recommendation_reason": ranking.recommendation_reason,
        "price_comparison": {
            "above_cheapest": ranking.price_above_cheapest,
            "below_expensive": ranking.price_below_most_expensive,
        }
    }


@router.get("/price-alerts/", tags=["Monitoring"])
async def list_price_alerts(
    db: Session = Depends(get_db),
    acknowledged: bool = False,
    limit: int = 50
):
    """List recent price alerts."""
    query = db.query(PriceAlert).filter(PriceAlert.is_acknowledged == acknowledged)
    alerts = query.order_by(PriceAlert.created_at.desc()).limit(limit).all()
    return alerts


@router.post("/price-alerts/{alert_id}/acknowledge", tags=["Monitoring"])
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge a price alert."""
    alert = db.query(PriceAlert).filter(PriceAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    from datetime import datetime
    alert.is_acknowledged = True
    alert.acknowledged_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Alert {alert_id} acknowledged")
    return alert
