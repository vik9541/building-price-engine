"""Database configuration and utilities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import redis
from typing import Generator
from app.config import settings

# PostgreSQL
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool,  # Avoid connection pool issues in Celery
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Database:
    """Database helper class."""
    
    @staticmethod
    def init() -> None:
        """Initialize database."""
        from app.models import Base
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def get_session() -> Session:
        """Get new database session."""
        return SessionLocal()
