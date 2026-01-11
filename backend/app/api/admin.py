"""Admin API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Competitor, ParseLog
from app.tasks import parse_competitors
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/parse/petrov")
async def parse_petrov(db: Session = Depends(get_db)):
    """Trigger Petrov.ru parsing."""
    task = parse_competitors.delay("petrov")
    return {"task_id": task.id, "status": "queued"}


@router.post("/parse/leroy")
async def parse_leroy(db: Session = Depends(get_db)):
    """Trigger Leroy Merlin parsing."""
    task = parse_competitors.delay("leroy_merlin")
    return {"task_id": task.id, "status": "queued"}


@router.post("/parse/obi")
async def parse_obi(db: Session = Depends(get_db)):
    """Trigger Obi parsing."""
    task = parse_competitors.delay("obi")
    return {"task_id": task.id, "status": "queued"}


@router.get("/parse/status")
async def parse_status(db: Session = Depends(get_db)):
    """Get parsing status."""
    # Get latest parse logs for each competitor
    petrov_log = db.query(ParseLog).filter(
        ParseLog.competitor_id == db.query(Competitor).filter(
            Competitor.competitor_type == "petrov"
        ).with_entities(Competitor.id).scalar()
    ).order_by(ParseLog.created_at.desc()).first()
    
    leroy_log = db.query(ParseLog).filter(
        ParseLog.competitor_id == db.query(Competitor).filter(
            Competitor.competitor_type == "leroy_merlin"
        ).with_entities(Competitor.id).scalar()
    ).order_by(ParseLog.created_at.desc()).first()
    
    obi_log = db.query(ParseLog).filter(
        ParseLog.competitor_id == db.query(Competitor).filter(
            Competitor.competitor_type == "obi"
        ).with_entities(Competitor.id).scalar()
    ).order_by(ParseLog.created_at.desc()).first()
    
    return {
        "petrov": petrov_log.dict() if petrov_log else None,
        "leroy_merlin": leroy_log.dict() if leroy_log else None,
        "obi": obi_log.dict() if obi_log else None,
    }
