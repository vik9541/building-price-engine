"""Celery tasks for updating prices."""
from celery import shared_task
from celery.beat import schedule
from app.database import SessionLocal
from app.models import Product
from app.pricing.strategy import calculate_price
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_all_prices():
    """Update prices for all products based on pricing strategy."""
    db = SessionLocal()
    
    try:
        logger.info("Starting price update")
        
        products = db.query(Product).filter(Product.is_active == True).all()
        updated_count = 0
        
        for product in products:
            try:
                new_price = calculate_price(product, db)
                if new_price and new_price != product.our_price:
                    product.our_price = new_price
                    updated_count += 1
            except Exception as e:
                logger.error(f"Error updating price for {product.sku}: {str(e)}")
                continue
        
        db.commit()
        logger.info(f"Price update completed. Updated {updated_count} products")
        
        return {"status": "success", "updated_count": updated_count}
    
    except Exception as e:
        logger.error(f"Price update error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
