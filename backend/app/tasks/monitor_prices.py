"""Celery tasks for continuous price monitoring."""
from celery import shared_task
from app.database import SessionLocal
from app.price_monitor.monitor import PriceMonitor
from app.models_extended import PriceSource
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@shared_task
def monitor_all_prices():
    """Monitor prices from all sources."""
    db = SessionLocal()
    
    try:
        logger.info("Starting comprehensive price monitoring")
        
        monitor = PriceMonitor(db)
        stats = monitor.monitor_all_products()
        
        logger.info(f"Price monitoring completed: {stats}")
        return {"status": "success", "stats": stats}
    
    except Exception as e:
        logger.error(f"Error in price monitoring: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@shared_task
def monitor_price_source(source_id: int):
    """Monitor specific price source."""
    db = SessionLocal()
    
    try:
        logger.info(f"Monitoring price source {source_id}")
        
        monitor = PriceMonitor(db)
        success = monitor.monitor_price_source(source_id)
        
        return {"status": "success" if success else "error", "source_id": source_id}
    
    except Exception as e:
        logger.error(f"Error monitoring source {source_id}: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@shared_task
def monitor_sources_round():
    """Monitor all price sources in sequence."""
    db = SessionLocal()
    
    try:
        logger.info("Starting price source monitoring round")
        
        # Get all active sources
        sources = db.query(PriceSource).filter(
            PriceSource.is_active == True
        ).all()
        
        results = []
        for source in sources:
            logger.info(f"Monitoring source: {source.name}")
            monitor = PriceMonitor(db)
            success = monitor.monitor_price_source(source.id)
            results.append({"source_id": source.id, "name": source.name, "success": success})
        
        logger.info(f"Monitoring round completed: {results}")
        return {"status": "success", "results": results}
    
    except Exception as e:
        logger.error(f"Error in monitoring round: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
