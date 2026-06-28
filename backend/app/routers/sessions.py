from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    PracticeLog,
    PracticeLogCreate,
    PracticeSession,
    PracticeSessionCreate,
    utc_now,
)

router = APIRouter(prefix="/practice-sessions", tags=["practice sessions"])


@router.get("", response_model=list[PracticeSession])
def list_practice_sessions(
    session: Session = Depends(get_session),
) -> list[PracticeSession]:
    return list(
        session.exec(
            select(PracticeSession).order_by(PracticeSession.session_date.desc())
        ).all()
    )


@router.post("", response_model=PracticeSession)
def create_practice_session(
    payload: PracticeSessionCreate, session: Session = Depends(get_session)
) -> PracticeSession:
    practice_session = PracticeSession.model_validate(payload)
    session.add(practice_session)
    session.commit()
    session.refresh(practice_session)
    return practice_session


@router.post("/{practice_session_id}/complete", response_model=PracticeSession)
def complete_practice_session(
    practice_session_id: int, session: Session = Depends(get_session)
) -> PracticeSession:
    practice_session = session.get(PracticeSession, practice_session_id)
    if practice_session is None:
        raise HTTPException(status_code=404, detail="Practice session not found")
    practice_session.status = "completed"
    practice_session.completed_at = utc_now()
    practice_session.session_date = date.today()
    session.add(practice_session)
    session.commit()
    session.refresh(practice_session)
    return practice_session


@router.post("/{practice_session_id}/logs", response_model=PracticeLog)
def create_practice_log(
    practice_session_id: int,
    payload: PracticeLogCreate,
    session: Session = Depends(get_session),
) -> PracticeLog:
    if practice_session_id != payload.session_id:
        raise HTTPException(status_code=400, detail="Session id mismatch")
    practice_session = session.get(PracticeSession, practice_session_id)
    if practice_session is None:
        raise HTTPException(status_code=404, detail="Practice session not found")
    log = PracticeLog.model_validate(payload)
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
