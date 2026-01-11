"""SQLAlchemy models for the application."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()


class CompetitorEnum(PyEnum):
    """Available competitors."""
    PETROV = "petrov"
    LEROY_MERLIN = "leroy_merlin"
    OBI = "obi"


class Product(Base):
    """Product catalog."""
    __tablename__ = "products"
    __table_args__ = (
        Index('idx_sku', 'sku'),
        Index('idx_category', 'category'),
        Index('idx_active', 'is_active'),
    )

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(200), index=True, nullable=False)
    subcategory = Column(String(200), nullable=True)
    
    # Pricing
    cost = Column(Float, nullable=False)  # Our cost
    our_price = Column(Float, nullable=False)  # Our selling price
    min_price = Column(Float, nullable=True)  # Min price from competitors
    max_price = Column(Float, nullable=True)  # Max price from competitors
    avg_competitor_price = Column(Float, nullable=True)  # Average competitor price
    
    # Images
    main_image_url = Column(String(500), nullable=True)
    images_json = Column(Text, nullable=True)  # JSON array of image URLs
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    competitor_prices = relationship("CompetitorPrice", back_populates="product", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    sales_stats = relationship("SalesStats", back_populates="product", uselist=False, cascade="all, delete-orphan")


class Competitor(Base):
    """Competitor information."""
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    competitor_type = Column(String(50), nullable=False)  # petrov, leroy_merlin, obi
    base_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    last_parsed = Column(DateTime, nullable=True)
    parse_status = Column(String(50), default="pending")  # pending, running, success, error
    parse_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    prices = relationship("CompetitorPrice", back_populates="competitor", cascade="all, delete-orphan")


class CompetitorPrice(Base):
    """Competitor prices for products."""
    __tablename__ = "competitor_prices"
    __table_args__ = (
        Index('idx_product_competitor', 'product_id', 'competitor_id'),
        Index('idx_timestamp', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False, index=True)
    
    competitor_sku = Column(String(100), nullable=True)  # SKU on competitor site
    competitor_url = Column(String(500), nullable=True)  # URL on competitor site
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)  # If discount is applied
    
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    product = relationship("Product", back_populates="competitor_prices")
    competitor = relationship("Competitor", back_populates="prices")


class PriceHistory(Base):
    """History of our price changes."""
    __tablename__ = "price_history"
    __table_args__ = (
        Index('idx_product_date', 'product_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    change_reason = Column(String(200), nullable=True)  # auto_pricing, manual, competitor_match
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    product = relationship("Product", back_populates="price_history")


class SalesStats(Base):
    """Sales statistics for products (for popularity-based pricing)."""
    __tablename__ = "sales_stats"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False, index=True)
    
    sales_count_week = Column(Integer, default=0)
    sales_count_month = Column(Integer, default=0)
    sales_count_total = Column(Integer, default=0)
    
    avg_rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)
    
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    product = relationship("Product", back_populates="sales_stats")


class PricingStrategy(Base):
    """Global pricing strategy settings."""
    __tablename__ = "pricing_strategies"

    id = Column(Integer, primary_key=True, index=True)
    
    # Markup ranges
    min_markup = Column(Float, default=10.0)  # Percentage
    max_markup = Column(Float, default=30.0)  # Percentage
    
    # Weights for pricing algorithm
    competitor_weight = Column(Float, default=0.7)  # How much to consider competitor prices
    popularity_weight = Column(Float, default=0.2)  # How much to consider product popularity
    
    # Minimum absolute margin
    min_margin_rub = Column(Float, default=50.0)  # Minimum profit in rubles
    
    # Competitor matching
    undercut_percentage = Column(Float, default=5.0)  # Undercut competitors by this %
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ParseLog(Base):
    """Parsing execution log."""
    __tablename__ = "parse_logs"
    __table_args__ = (
        Index('idx_competitor_date', 'competitor_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=True)
    
    status = Column(String(50), nullable=False)  # success, error, partial
    products_processed = Column(Integer, default=0)
    products_added = Column(Integer, default=0)
    products_updated = Column(Integer, default=0)
    
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class User(Base):
    """Admin users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
