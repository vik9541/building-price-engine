"""Price aggregation and analysis from multiple sources."""
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from statistics import mean, median, stdev
import numpy as np

from app.models import Product, CompetitorPrice
from app.models_extended import (
    PriceSnapshot, PriceSource, ProductSourceMapping, 
    MarketAnalysis, PriceAlert, CompetitorPriceRanking
)
from app.config import settings

logger = logging.getLogger(__name__)


class PriceAggregator:
    """Aggregate and analyze prices from multiple sources."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_product_market(self, product_id: int) -> Optional[MarketAnalysis]:
        """Analyze market for a specific product."""
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                logger.error(f"Product not found: {product_id}")
                return None
            
            # Get all competitor prices for this product
            competitor_prices = self.db.query(CompetitorPrice).filter(
                CompetitorPrice.product_id == product_id,
                CompetitorPrice.in_stock == True,
            ).all()
            
            if not competitor_prices:
                logger.warning(f"No competitor prices found for {product.sku}")
                return None
            
            prices = [cp.price for cp in competitor_prices if cp.price > 0]
            
            if not prices:
                return None
            
            # Calculate statistics
            price_min = min(prices)
            price_max = max(prices)
            price_avg = mean(prices)
            price_median = median(prices)
            price_std_dev = stdev(prices) if len(prices) > 1 else 0.0
            
            # Determine our market position
            our_price = product.our_price
            our_position = self._determine_position(our_price, prices)
            our_percentile = (sum(1 for p in prices if p <= our_price) / len(prices)) * 100
            
            # Get Yandex Market price if available
            yandex_price = self._get_yandex_market_price(product_id)
            yandex_deviation = None
            if yandex_price:
                yandex_deviation = ((our_price - yandex_price) / yandex_price) * 100
            
            # Price trends
            trends = self._calculate_price_trends(product_id)
            
            # Create or update analysis
            analysis = self.db.query(MarketAnalysis).filter(
                MarketAnalysis.product_id == product_id
            ).first()
            
            if not analysis:
                analysis = MarketAnalysis(product_id=product_id)
            
            analysis.active_sellers_count = len(prices)
            analysis.price_min = price_min
            analysis.price_max = price_max
            analysis.price_avg = price_avg
            analysis.price_median = price_median
            analysis.price_std_dev = price_std_dev
            analysis.our_position = our_position
            analysis.our_price_percentile = our_percentile
            analysis.yandex_market_price = yandex_price
            analysis.yandex_market_deviation = yandex_deviation
            analysis.price_trend = trends['trend']
            analysis.price_trend_24h = trends['trend_24h']
            analysis.price_trend_7d = trends['trend_7d']
            analysis.price_trend_30d = trends['trend_30d']
            analysis.analysis_date = datetime.utcnow()
            
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            
            logger.info(f"Market analysis completed for {product.sku}")
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing market for product {product_id}: {str(e)}")
            return None
    
    def create_price_ranking(self, product_id: int) -> Optional[CompetitorPriceRanking]:
        """Create price ranking compared to competitors."""
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            
            # Get competitor prices
            competitor_prices = self.db.query(CompetitorPrice).filter(
                CompetitorPrice.product_id == product_id,
                CompetitorPrice.in_stock == True,
            ).all()
            
            if not competitor_prices:
                return None
            
            prices = sorted([cp.price for cp in competitor_prices if cp.price > 0])
            our_price = product.our_price
            
            # Find our rank
            our_rank = 1
            for i, price in enumerate(prices, 1):
                if price > our_price:
                    our_rank = i
                    break
            else:
                our_rank = len(prices) + 1
            
            # Calculate differences
            cheapest = min(prices)
            most_expensive = max(prices)
            price_above_cheapest = our_price - cheapest
            price_below_expensive = most_expensive - our_price
            
            # Recommend optimal price
            recommended_price = self._calculate_optimal_price(prices, product)
            reason = self._get_recommendation_reason(our_price, prices, recommended_price)
            
            # Create or update ranking
            ranking = self.db.query(CompetitorPriceRanking).filter(
                CompetitorPriceRanking.product_id == product_id
            ).first()
            
            if not ranking:
                ranking = CompetitorPriceRanking(product_id=product_id)
            
            ranking.total_competitors = len(prices)
            ranking.our_rank = our_rank
            ranking.price_above_cheapest = price_above_cheapest
            ranking.price_below_most_expensive = price_below_expensive
            ranking.recommended_price = recommended_price
            ranking.recommendation_reason = reason
            ranking.analysis_date = datetime.utcnow()
            
            self.db.add(ranking)
            self.db.commit()
            self.db.refresh(ranking)
            
            logger.info(f"Price ranking created for {product.sku}: rank {our_rank}/{len(prices)}")
            return ranking
        
        except Exception as e:
            logger.error(f"Error creating price ranking for {product_id}: {str(e)}")
            return None
    
    def detect_price_anomalies(self, product_id: int) -> List[str]:
        """Detect unusual price patterns."""
        anomalies = []
        
        try:
            analysis = self.db.query(MarketAnalysis).filter(
                MarketAnalysis.product_id == product_id
            ).order_by(MarketAnalysis.analysis_date.desc()).first()
            
            if not analysis or not analysis.price_std_dev:
                return anomalies
            
            # Check for extreme deviations
            if analysis.price_std_dev > analysis.price_avg * 0.5:  # High variance
                anomalies.append("high_price_variance")
            
            # Check for significant trend
            if analysis.price_trend_24h and abs(analysis.price_trend_24h) > 10:
                anomalies.append("sharp_price_movement")
            
            # Check if we're outlier
            if analysis.our_price_percentile and (
                analysis.our_price_percentile < 10 or analysis.our_price_percentile > 90
            ):
                anomalies.append("price_outlier")
            
            # Check Yandex deviation
            if analysis.yandex_market_deviation and abs(analysis.yandex_market_deviation) > 20:
                anomalies.append("yandex_market_deviation")
        
        except Exception as e:
            logger.error(f"Error detecting anomalies for {product_id}: {str(e)}")
        
        return anomalies
    
    def _determine_position(self, our_price: float, market_prices: List[float]) -> str:
        """Determine our position in market."""
        if not market_prices:
            return "unknown"
        
        sorted_prices = sorted(market_prices)
        avg = mean(sorted_prices)
        
        if our_price <= sorted_prices[0]:
            return "cheapest"
        elif our_price >= sorted_prices[-1]:
            return "most_expensive"
        elif our_price <= avg * 0.95:
            return "below_median"
        elif our_price >= avg * 1.05:
            return "above_median"
        else:
            return "median"
    
    def _get_yandex_market_price(self, product_id: int) -> Optional[float]:
        """Get Yandex Market price if available."""
        # TODO: Implement Yandex Market API integration
        return None
    
    def _calculate_price_trends(self, product_id: int) -> Dict[str, Optional[float]]:
        """Calculate price trends over different periods."""
        trends = {
            'trend': 'stable',
            'trend_24h': None,
            'trend_7d': None,
            'trend_30d': None,
        }
        
        try:
            now = datetime.utcnow()
            
            # Get snapshots for different periods
            snapshot_24h_ago = now - timedelta(hours=24)
            snapshot_7d_ago = now - timedelta(days=7)
            snapshot_30d_ago = now - timedelta(days=30)
            
            current = self.db.query(func.avg(PriceSnapshot.price)).filter(
                PriceSnapshot.product_id == product_id,
                PriceSnapshot.snapshot_date >= now - timedelta(hours=1)
            ).scalar()
            
            if current:
                # 24h trend
                old_24h = self.db.query(func.avg(PriceSnapshot.price)).filter(
                    PriceSnapshot.product_id == product_id,
                    PriceSnapshot.snapshot_date.between(snapshot_24h_ago, snapshot_24h_ago + timedelta(hours=1))
                ).scalar()
                if old_24h:
                    trends['trend_24h'] = ((current - old_24h) / old_24h) * 100
                
                # 7d trend
                old_7d = self.db.query(func.avg(PriceSnapshot.price)).filter(
                    PriceSnapshot.product_id == product_id,
                    PriceSnapshot.snapshot_date.between(snapshot_7d_ago, snapshot_7d_ago + timedelta(hours=1))
                ).scalar()
                if old_7d:
                    trends['trend_7d'] = ((current - old_7d) / old_7d) * 100
                
                # 30d trend
                old_30d = self.db.query(func.avg(PriceSnapshot.price)).filter(
                    PriceSnapshot.product_id == product_id,
                    PriceSnapshot.snapshot_date.between(snapshot_30d_ago, snapshot_30d_ago + timedelta(hours=1))
                ).scalar()
                if old_30d:
                    trends['trend_30d'] = ((current - old_30d) / old_30d) * 100
                
                # Determine trend direction
                if trends['trend_7d']:
                    if trends['trend_7d'] > 5:
                        trends['trend'] = 'up'
                    elif trends['trend_7d'] < -5:
                        trends['trend'] = 'down'
        
        except Exception as e:
            logger.error(f"Error calculating trends for {product_id}: {str(e)}")
        
        return trends
    
    def _calculate_optimal_price(self, market_prices: List[float], product: Product) -> float:
        """Calculate optimal price based on market data."""
        if not market_prices:
            return product.our_price
        
        avg_price = mean(market_prices)
        min_price = min(market_prices)
        
        # Strategy: undercut average by small margin
        optimal_price = avg_price * 0.98
        
        # But ensure minimum margin
        min_acceptable = product.cost + settings.min_margin_rub
        optimal_price = max(optimal_price, min_acceptable)
        
        # Ensure maximum markup
        max_acceptable = product.cost * (1 + settings.markup_max / 100)
        optimal_price = min(optimal_price, max_acceptable)
        
        return round(optimal_price, 2)
    
    def _get_recommendation_reason(self, our_price: float, market_prices: List[float], recommended: float) -> str:
        """Get reason for price recommendation."""
        avg = mean(market_prices)
        min_price = min(market_prices)
        max_price = max(market_prices)
        
        if our_price > max_price:
            return "Our price is highest. Recommend lowering to stay competitive."
        elif our_price < min_price:
            return "Our price is lowest. Can increase while remaining competitive."
        elif our_price > avg:
            return "Our price is above average. Consider lowering to match market."
        elif our_price < avg:
            return "Our price is below average. Good competitive position."
        else:
            return "Price is at market average. Consider undercutting for more sales."
