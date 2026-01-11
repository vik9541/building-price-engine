"""Real-time price monitoring service."""
import logging
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Product, CompetitorPrice, PricingStrategy
from app.models_extended import (
    PriceSnapshot, PriceSource, ProductSourceMapping,
    MarketAnalysis, PriceAlert
)
from app.config import settings
from app.price_monitor.aggregator import PriceAggregator

logger = logging.getLogger(__name__)


class PriceMonitor:
    """Monitor prices from multiple sources in real-time."""
    
    def __init__(self, db: Session):
        self.db = db
        self.aggregator = PriceAggregator(db)
    
    def monitor_all_products(self) -> Dict[str, int]:
        """Monitor prices for all active products."""
        stats = {
            'total_products': 0,
            'products_analyzed': 0,
            'prices_updated': 0,
            'alerts_created': 0,
        }
        
        try:
            # Get all active products
            products = self.db.query(Product).filter(
                Product.is_active == True
            ).all()
            
            stats['total_products'] = len(products)
            logger.info(f"Starting price monitoring for {len(products)} products")
            
            for product in products:
                try:
                    # Analyze market
                    analysis = self.aggregator.analyze_product_market(product.id)
                    if analysis:
                        stats['products_analyzed'] += 1
                    
                    # Check for price changes and create alerts
                    alerts = self._check_price_changes(product.id)
                    stats['alerts_created'] += len(alerts)
                    
                    # Update pricing based on market analysis
                    updated = self._update_product_price(product.id)
                    if updated:
                        stats['prices_updated'] += 1
                
                except Exception as e:
                    logger.error(f"Error monitoring product {product.sku}: {str(e)}")
                    continue
            
            logger.info(f"Price monitoring completed: {stats}")
            return stats
        
        except Exception as e:
            logger.error(f"Error in price monitoring: {str(e)}")
            return stats
    
    def monitor_price_source(self, source_id: int) -> bool:
        """Monitor prices from specific source."""
        try:
            source = self.db.query(PriceSource).filter(
                PriceSource.id == source_id,
                PriceSource.is_active == True
            ).first()
            
            if not source:
                logger.error(f"Price source not found: {source_id}")
                return False
            
            logger.info(f"Starting monitoring for source: {source.name}")
            
            # Update monitoring status
            source.check_status = "running"
            source.last_checked = datetime.utcnow()
            self.db.commit()
            
            # Get all mapped products for this source
            mappings = self.db.query(ProductSourceMapping).filter(
                ProductSourceMapping.price_source_id == source_id,
                ProductSourceMapping.is_active == True
            ).all()
            
            logger.info(f"Found {len(mappings)} product mappings for {source.name}")
            
            updated_count = 0
            for mapping in mappings:
                try:
                    # Update price snapshot
                    if mapping.last_price:
                        snapshot = PriceSnapshot(
                            product_id=mapping.product_id,
                            price_source_id=source_id,
                            price=mapping.last_price,
                            snapshot_date=datetime.utcnow()
                        )
                        self.db.add(snapshot)
                        updated_count += 1
                
                except Exception as e:
                    logger.error(f"Error updating snapshot for mapping {mapping.id}: {str(e)}")
                    continue
            
            self.db.commit()
            source.check_status = "success"
            source.last_error = None
            self.db.commit()
            
            logger.info(f"Updated {updated_count} price snapshots for {source.name}")
            return True
        
        except Exception as e:
            logger.error(f"Error monitoring source {source_id}: {str(e)}")
            source = self.db.query(PriceSource).filter(PriceSource.id == source_id).first()
            if source:
                source.check_status = "error"
                source.last_error = str(e)
                self.db.commit()
            return False
    
    def _check_price_changes(self, product_id: int) -> List[PriceAlert]:
        """Check for significant price changes."""
        alerts = []
        
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return alerts
            
            # Get current competitor prices
            current_prices = self.db.query(CompetitorPrice).filter(
                CompetitorPrice.product_id == product_id
            ).all()
            
            # Get last known prices
            last_snapshot_date = datetime.utcnow()
            last_snapshots = self.db.query(PriceSnapshot).filter(
                PriceSnapshot.product_id == product_id,
                PriceSnapshot.snapshot_date < last_snapshot_date
            ).order_by(PriceSnapshot.snapshot_date.desc()).limit(10).all()
            
            for current in current_prices:
                # Find corresponding last snapshot
                last = next(
                    (s for s in last_snapshots if s.price_source_id == current.competitor_id),
                    None
                )
                
                if last:
                    # Check for significant change
                    change_percent = ((current.price - last.price) / last.price) * 100
                    
                    # Alert on >10% change
                    if abs(change_percent) > 10:
                        alert_type = "price_drop" if change_percent < 0 else "price_spike"
                        
                        alert = PriceAlert(
                            product_id=product_id,
                            price_source_id=current.competitor_id,
                            alert_type=alert_type,
                            old_price=last.price,
                            new_price=current.price,
                            change_percent=change_percent,
                            message=f"Price {'decreased' if change_percent < 0 else 'increased'} "
                                   f"by {abs(change_percent):.1f}% from {last.price} to {current.price}"
                        )
                        self.db.add(alert)
                        alerts.append(alert)
                        logger.warning(f"Price alert for {product.sku}: {alert.message}")
            
            self.db.commit()
        
        except Exception as e:
            logger.error(f"Error checking price changes for {product_id}: {str(e)}")
        
        return alerts
    
    def _update_product_price(self, product_id: int) -> bool:
        """Update product price based on market analysis."""
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            
            # Get market analysis
            analysis = self.db.query(MarketAnalysis).filter(
                MarketAnalysis.product_id == product_id
            ).order_by(MarketAnalysis.analysis_date.desc()).first()
            
            if not analysis:
                return False
            
            # Create ranking
            ranking = self.aggregator.create_price_ranking(product_id)
            if not ranking or not ranking.recommended_price:
                return False
            
            # Check if we should update price
            current_price = product.our_price
            recommended_price = ranking.recommended_price
            
            # Only update if difference is > 5 rubles or > 2%
            price_diff = abs(recommended_price - current_price)
            price_diff_percent = (price_diff / current_price) * 100 if current_price > 0 else 0
            
            if price_diff > 5 or price_diff_percent > 2:
                logger.info(
                    f"Updating price for {product.sku}: "
                    f"{current_price} -> {recommended_price} (reason: {ranking.recommendation_reason})"
                )
                product.our_price = recommended_price
                self.db.commit()
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error updating price for product {product_id}: {str(e)}")
            return False
