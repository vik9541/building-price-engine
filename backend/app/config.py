"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/building_db"
    redis_url: str = "redis://localhost:6379/0"
    
    # API
    api_title: str = "Building Price Engine API"
    api_version: str = "1.0.0"
    api_workers: int = 4
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    debug: bool = False
    cors_origins: List[str] = ["*"]
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Admin
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # Parsers URLs
    petrov_url: str = "https://www.petrov.ru"
    leroy_url: str = "https://www.leroymerlin.ru"
    obi_url: str = "https://www.obi.ru"
    
    # Parsing Schedule (minutes)
    parse_interval: int = 60
    price_check_interval: int = 30
    price_calculate_interval: int = 60
    
    # Pricing Strategy
    markup_min: float = 10.0
    markup_max: float = 30.0
    competitor_weight: float = 0.7
    popularity_weight: float = 0.2
    min_margin_rub: float = 50.0
    
    # Image Storage
    image_storage_path: str = "/app/storage/images"
    image_max_size_mb: int = 10
    
    # Parser Settings
    parser_user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    parser_timeout: int = 30
    parser_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_path: str = "/app/logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
