"""Celery tasks for parsing competitors."""
from celery import shared_task
from app.database import SessionLocal
from app.models import Competitor, ParseLog, Product, CompetitorPrice
from app.config import settings
import logging
from datetime import datetime
from time import time

logger = logging.getLogger(__name__)


@shared_task
def parse_competitors(competitor_type: str):
    """Parse competitor products and prices."""
    db = SessionLocal()
    start_time = time()
    
    try:
        logger.info(f"Starting parse for {competitor_type}")
        
        # Get competitor
        competitor = db.query(Competitor).filter(
            Competitor.competitor_type == competitor_type
        ).first()
        
        if not competitor:
            logger.error(f"Competitor not found: {competitor_type}")
            return {"status": "error", "message": "Competitor not found"}
        
        # Update competitor status
        competitor.parse_status = "running"
        competitor.last_parsed = datetime.utcnow()
        db.commit()
        
        # TODO: Implement actual parsing logic here
        # For now, just return success
        
        products_processed = 0
        products_added = 0
        products_updated = 0
        
        # Log parse result
        duration = time() - start_time
        parse_log = ParseLog(
            competitor_id=competitor.id,
            status="success",
            products_processed=products_processed,
            products_added=products_added,
            products_updated=products_updated,
            duration_seconds=duration,
        )
        db.add(parse_log)
        
        competitor.parse_status = "success"
        competitor.parse_error = None
        db.commit()
        
        logger.info(f"Parse completed for {competitor_type} in {duration:.2f}s")
        
        return {
            "status": "success",
            "products_processed": products_processed,
            "products_added": products_added,
            "products_updated": products_updated,
            "duration": duration,
        }
    
    except Exception as e:
        logger.error(f"Parse error for {competitor_type}: {str(e)}")
        
        # Update competitor status
        competitor = db.query(Competitor).filter(
            Competitor.competitor_type == competitor_type
        ).first()
        if competitor:
            competitor.parse_status = "error"
            competitor.parse_error = str(e)
            
            # Log parse error
            duration = time() - start_time
            parse_log = ParseLog(
                competitor_id=competitor.id,
                status="error",
                error_message=str(e),
                duration_seconds=duration,
            )
            db.add(parse_log)
            db.commit()
        
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
