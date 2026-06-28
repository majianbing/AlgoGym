from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from app.database import get_session
from app.models import Document, PatternMastery, PracticeSession

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def read_dashboard(session: Session = Depends(get_session)) -> dict[str, int | float]:
    documents = session.exec(select(func.count()).select_from(Document)).one()
    completed = session.exec(
        select(PracticeSession).where(PracticeSession.status == "completed")
    ).all()
    mastery = session.exec(select(PatternMastery)).all()

    completed_dates = {item.session_date for item in completed}
    streak = 0
    cursor = date.today()
    while cursor in completed_dates:
        streak += 1
        cursor -= timedelta(days=1)

    average_confidence = (
        sum(item.confidence for item in mastery) / len(mastery) if mastery else 0
    )

    return {
        "documents": documents,
        "completed_sessions": len(completed),
        "current_streak": streak,
        "tracked_patterns": len(mastery),
        "average_confidence": round(average_confidence, 1),
    }
