"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import Database
from app.api import products, competitors, prices, admin

# Setup logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up...")
    Database.init()
    yield
    # Shutdown
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        lifespan=lifespan,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Routes
    app.include_router(products.router, prefix="/api/products", tags=["Products"])
    app.include_router(competitors.router, prefix="/api/competitors", tags=["Competitors"])
    app.include_router(prices.router, prefix="/api/prices", tags=["Prices"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
    
    @app.get("/")
    async def root():
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "status": "running"
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    logger.info("Application created successfully")
    return app


app = create_app()
