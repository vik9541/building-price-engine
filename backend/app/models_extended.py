"""Extended models for competitive price analysis."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from app.models import Base


class PriceSnapshot(Base):
    """Historical price snapshot for analysis and trends."""
    __tablename__ = "price_snapshots"
    __table_args__ = (
        Index('idx_product_date', 'product_id', 'snapshot_date'),
        Index('idx_source_date', 'price_source_id', 'snapshot_date'),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    price_source_id = Column(Integer, ForeignKey("price_sources.id"), nullable=False, index=True)
    
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="RUB")
    in_stock = Column(Boolean, default=True)
    
    # Market position
    market_position = Column(String(20))  # cheapest, most_expensive, median, above_median, below_median
    deviation_from_avg = Column(Float, nullable=True)  # % deviation from market average
    
    snapshot_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    product = relationship("Product", foreign_keys=[product_id])
    price_source = relationship("PriceSource", foreign_keys=[price_source_id])


class PriceSource(Base):
    """Price source (marketplace, shop, etc)."""
    __tablename__ = "price_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    source_type = Column(String(50), nullable=False)  # yandex_market, avangard, e-catalog, etc
    base_url = Column(String(500), nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_reliable = Column(Boolean, default=True)  # Consider in price calculations
    
    # Weight in calculations (0.0 to 1.0)
    # Reliable sources get higher weight
    weight = Column(Float, default=1.0)
    
    # Monitoring settings
    check_interval_minutes = Column(Integer, default=60)  # How often to check
    last_checked = Column(DateTime, nullable=True)
    check_status = Column(String(50), default="pending")  # pending, running, success, error
    last_error = Column(Text, nullable=True)
    
    # Statistics
    total_products_tracked = Column(Integer, default=0)
    price_updates_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    price_snapshots = relationship("PriceSnapshot", back_populates="price_source", cascade="all, delete-orphan")
    product_mappings = relationship("ProductSourceMapping", back_populates="price_source", cascade="all, delete-orphan")


class ProductSourceMapping(Base):
    """Mapping between our products and competitor products."""
    __tablename__ = "product_source_mappings"
    __table_args__ = (
        Index('idx_product_source', 'product_id', 'price_source_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    price_source_id = Column(Integer, ForeignKey("price_sources.id"), nullable=False, index=True)
    
    # How we found/matched this product
    source_product_id = Column(String(200), nullable=False)  # SKU/ID in source
    source_product_url = Column(String(1000), nullable=True)  # URL in source
    source_product_name = Column(String(500), nullable=True)  # Name in source
    
    # Matching quality
    match_score = Column(Float, nullable=True)  # 0-100, how confident we are
    match_method = Column(String(50))  # sku_match, name_match, manual, api
    
    is_active = Column(Boolean, default=True)
    
    # Last known price
    last_price = Column(Float, nullable=True)
    last_price_update = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    product = relationship("Product", foreign_keys=[product_id])
    price_source = relationship("PriceSource", foreign_keys=[price_source_id])


class MarketAnalysis(Base):
    """Market analysis for each product."""
    __tablename__ = "market_analysis"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False, index=True)
    
    # Market data
    active_sellers_count = Column(Integer, default=0)  # How many sellers have this product
    
    # Price statistics
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    price_avg = Column(Float, nullable=True)
    price_median = Column(Float, nullable=True)
    price_std_dev = Column(Float, nullable=True)  # Standard deviation
    
    # Price distribution
    price_distribution = Column(JSON, nullable=True)  # {"100-200": 5, "200-300": 10}
    
    # Market position
    our_position = Column(String(50))  # cheapest, expensive, median, etc
    our_price_percentile = Column(Float, nullable=True)  # 0-100
    
    # Trends
    price_trend = Column(String(50))  # up, down, stable
    price_trend_24h = Column(Float, nullable=True)  # % change
    price_trend_7d = Column(Float, nullable=True)  # % change
    price_trend_30d = Column(Float, nullable=True)  # % change
    
    # Reliability
    yandex_market_price = Column(Float, nullable=True)
    yandex_market_deviation = Column(Float, nullable=True)  # % deviation
    is_price_stable = Column(Boolean, default=True)  # No wild price swings
    
    analysis_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    product = relationship("Product", foreign_keys=[product_id])


class PriceAlert(Base):
    """Alerts for significant price changes."""
    __tablename__ = "price_alerts"
    __table_args__ = (
        Index('idx_product_date', 'product_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    price_source_id = Column(Integer, ForeignKey("price_sources.id"), nullable=False)
    
    alert_type = Column(String(50), nullable=False)  # price_drop, price_spike, competitor_undercut, stock_change
    
    old_price = Column(Float, nullable=True)
    new_price = Column(Float, nullable=True)
    change_percent = Column(Float, nullable=True)
    
    message = Column(Text, nullable=True)
    is_acknowledged = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Relations
    product = relationship("Product", foreign_keys=[product_id])
    price_source = relationship("PriceSource", foreign_keys=[price_source_id])


class CompetitorPriceRanking(Base):
    """Ranking of our price vs competitors for each product."""
    __tablename__ = "competitor_price_rankings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False, index=True)
    
    # Ranking data
    total_competitors = Column(Integer, default=0)
    our_rank = Column(Integer, nullable=True)  # 1 = cheapest, N = most expensive
    
    # Price comparison
    price_above_cheapest = Column(Float, nullable=True)  # Our price - cheapest price
    price_below_most_expensive = Column(Float, nullable=True)  # Most expensive - our price
    
    # Recommendations
    recommended_price = Column(Float, nullable=True)
    recommendation_reason = Column(Text, nullable=True)
    
    analysis_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    product = relationship("Product", foreign_keys=[product_id])
