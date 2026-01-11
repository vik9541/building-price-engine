"""Pricing strategy implementation."""
from app.models import Product, CompetitorPrice, PricingStrategy
from app.database import SessionLocal
from sqlalchemy.orm import Session
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def calculate_price(
    product: Product,
    db: Session,
    strategy: Optional[PricingStrategy] = None,
) -> Optional[float]:
    """Calculate optimal price for product."""
    
    if not strategy:
        strategy = db.query(PricingStrategy).filter(
            PricingStrategy.is_active == True
        ).first()
    
    if not strategy:
        logger.error("No active pricing strategy found")
        return None
    
    # Base price with minimum markup
    base_price = product.cost * (1 + strategy.min_markup / 100)
    
    # Get competitor prices
    competitor_prices = db.query(CompetitorPrice).filter(
        CompetitorPrice.product_id == product.id,
        CompetitorPrice.in_stock == True,
    ).all()
    
    if not competitor_prices:
        logger.debug(f"No competitor prices for {product.sku}, using base price")
        return max(base_price, product.cost + strategy.min_margin_rub)
    
    # Calculate average competitor price
    prices = [cp.price for cp in competitor_prices]
    avg_competitor_price = sum(prices) / len(prices)
    min_competitor_price = min(prices)
    max_competitor_price = max(prices)
    
    # Update product with competitor price stats
    product.min_price = min_competitor_price
    product.max_price = max_competitor_price
    product.avg_competitor_price = avg_competitor_price
    
    # Pricing logic
    final_price = base_price
    
    # Consider competitor prices
    if avg_competitor_price > base_price * 1.15:
        # Competitors are much more expensive - we can increase price
        final_price = avg_competitor_price * 0.95  # Undercut by 5%
    elif avg_competitor_price < base_price * 0.85:
        # Competitors are much cheaper - we need to match
        final_price = avg_competitor_price * 1.02  # Slight premium
    else:
        # Competitors are close to our price
        final_price = max(base_price, avg_competitor_price * 0.98)
    
    # Ensure minimum margin
    min_price = product.cost + strategy.min_margin_rub
    final_price = max(final_price, min_price)
    
    # Ensure maximum markup
    max_price = product.cost * (1 + strategy.max_markup / 100)
    final_price = min(final_price, max_price)
    
    logger.debug(
        f"Calculated price for {product.sku}: "
        f"cost={product.cost}, "
        f"competitors_avg={avg_competitor_price:.2f}, "
        f"final_price={final_price:.2f}"
    )
    
    return final_price
