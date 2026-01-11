"""Competitors API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Competitor
from app import schemas
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[schemas.CompetitorRead])
async def list_competitors(db: Session = Depends(get_db)):
    """List all competitors."""
    competitors = db.query(Competitor).all()
    return competitors


@router.get("/{competitor_id}", response_model=schemas.CompetitorRead)
async def get_competitor(competitor_id: int, db: Session = Depends(get_db)):
    """Get competitor by ID."""
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor
