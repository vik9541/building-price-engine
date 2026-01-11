"""Analyze Yandex Market prices for validation."""
import logging
from typing import Optional, Dict
import requests
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Product
from app.models_extended import MarketAnalysis
from app.config import settings

logger = logging.getLogger(__name__)


class YandexMarketAnalyzer:
    """Analyze prices on Yandex Market as benchmark."""
    
    def __init__(self):
        self.base_url = "https://api.partner.market.yandex.ru"
        # TODO: Add Yandex Market API credentials to settings
    
    def get_market_price(self, product_name: str, product_sku: str) -> Optional[Dict]:
        """Get Yandex Market price for product."""
        try:
            # This is a placeholder - actual implementation requires Yandex API
            logger.debug(f"Searching Yandex Market for: {product_name}")
            
            # Real implementation would:
            # 1. Search product on Yandex Market
            # 2. Get price range
            # 3. Get seller count
            # 4. Calculate average
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting Yandex Market price: {str(e)}")
            return None
    
    def validate_prices(self, product_id: int, db: Session) -> bool:
        """Validate that our and competitor prices match Yandex Market."""
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            
            analysis = db.query(MarketAnalysis).filter(
                MarketAnalysis.product_id == product_id
            ).order_by(MarketAnalysis.analysis_date.desc()).first()
            
            if not analysis or not analysis.yandex_market_price:
                logger.debug(f"No Yandex Market data for {product.sku}")
                return True
            
            # Check deviation
            if analysis.yandex_market_deviation is None:
                return True
            
            # Prices with >30% deviation are suspicious
            if abs(analysis.yandex_market_deviation) > 30:
                logger.warning(
                    f"Large deviation for {product.sku}: "
                    f"Our={analysis.yandex_market_price}, "
                    f"Deviation={analysis.yandex_market_deviation}%"
                )
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating prices: {str(e)}")
            return False
