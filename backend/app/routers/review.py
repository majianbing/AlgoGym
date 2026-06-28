from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    Mistake,
    MistakeCreate,
    PatternMastery,
    PatternMasteryUpsert,
    utc_now,
)

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/mistakes", response_model=list[Mistake])
def list_mistakes(session: Session = Depends(get_session)) -> list[Mistake]:
    return list(session.exec(select(Mistake).order_by(Mistake.created_at.desc())).all())


@router.post("/mistakes", response_model=Mistake)
def create_mistake(
    payload: MistakeCreate, session: Session = Depends(get_session)
) -> Mistake:
    mistake = Mistake.model_validate(payload)
    session.add(mistake)
    session.commit()
    session.refresh(mistake)
    return mistake


@router.get("/mastery", response_model=list[PatternMastery])
def list_mastery(session: Session = Depends(get_session)) -> list[PatternMastery]:
    return list(session.exec(select(PatternMastery).order_by(PatternMastery.pattern)).all())


@router.put("/mastery/{pattern}", response_model=PatternMastery)
def upsert_mastery(
    pattern: str,
    payload: PatternMasteryUpsert,
    session: Session = Depends(get_session),
) -> PatternMastery:
    existing = session.exec(
        select(PatternMastery).where(PatternMastery.pattern == pattern)
    ).first()
    if existing is None:
        existing = PatternMastery.model_validate(payload)
    else:
        existing.level = payload.level
        existing.confidence = payload.confidence
        existing.notes = payload.notes
        existing.updated_at = utc_now()
    existing.pattern = pattern
    existing.last_practiced_at = utc_now()
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing
