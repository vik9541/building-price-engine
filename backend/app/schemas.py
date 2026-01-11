"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# Product schemas
class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    cost: float
    our_price: float
    main_image_url: Optional[str] = None
    images_json: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    cost: Optional[float] = None
    our_price: Optional[float] = None
    is_active: Optional[bool] = None
    main_image_url: Optional[str] = None


class ProductRead(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    category: str
    subcategory: Optional[str]
    cost: float
    our_price: float
    min_price: Optional[float]
    max_price: Optional[float]
    avg_competitor_price: Optional[float]
    main_image_url: Optional[str]
    is_active: bool
    last_synced: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Competitor schemas
class CompetitorRead(BaseModel):
    id: int
    name: str
    competitor_type: str
    base_url: str
    is_active: bool
    last_parsed: Optional[datetime]
    parse_status: str
    parse_error: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Price schemas
class CompetitorPriceRead(BaseModel):
    id: int
    product_id: int
    competitor_id: int
    price: float
    old_price: Optional[float]
    in_stock: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Pricing strategy schemas
class PricingStrategyRead(BaseModel):
    id: int
    min_markup: float
    max_markup: float
    competitor_weight: float
    popularity_weight: float
    min_margin_rub: float
    undercut_percentage: float
    is_active: bool
    
    class Config:
        from_attributes = True


class PricingStrategyUpdate(BaseModel):
    min_markup: Optional[float] = None
    max_markup: Optional[float] = None
    competitor_weight: Optional[float] = None
    popularity_weight: Optional[float] = None
    min_margin_rub: Optional[float] = None
    undercut_percentage: Optional[float] = None
