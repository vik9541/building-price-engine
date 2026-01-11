"""Maintenance tasks."""
from celery import shared_task
from app.database import SessionLocal
from app.models_extended import PriceAlert, PriceSnapshot
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_alerts():
    """Remove alerts older than 30 days."""
    db = SessionLocal()
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        deleted = db.query(PriceAlert).filter(
            PriceAlert.created_at < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(f"Deleted {deleted} old price alerts")
        
        return {"status": "success", "deleted": deleted}
    
    except Exception as e:
        logger.error(f"Error cleaning up alerts: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@shared_task
def cleanup_old_snapshots():
    """Remove price snapshots older than 90 days."""
    db = SessionLocal()
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        
        deleted = db.query(PriceSnapshot).filter(
            PriceSnapshot.snapshot_date < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(f"Deleted {deleted} old price snapshots")
        
        return {"status": "success", "deleted": deleted}
    
    except Exception as e:
        logger.error(f"Error cleaning up snapshots: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
