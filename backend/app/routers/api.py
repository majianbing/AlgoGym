from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_session
from app.models import AppSetting, Document, PracticeSession, Problem, Streak, WeakPattern, utc_now
from app.schemas import (
    FinishSessionRequest,
    HintRequest,
    PlanGenerateRequest,
    SettingsPayload,
    StartSessionRequest,
)
from app.services.coach import CoachService
from app.services.ingestion import ingest_document, save_markdown_upload
from app.services.review_scheduler import next_review_date
from app.services.seeds import curriculum_by_week
from app.services.serialization import document_to_dict, session_to_dict, weak_pattern_to_dict

router = APIRouter(prefix="/api")


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        filename, path, content = await save_markdown_upload(file, get_settings())
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 markdown") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    document = Document(filename=filename, content=content, source_path=path)
    session.add(document)
    session.commit()
    session.refresh(document)
    return document_to_dict(document)


@router.get("/documents")
def list_documents(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    documents = session.scalars(select(Document).order_by(Document.created_at.desc())).all()
    return [document_to_dict(document) for document in documents]


@router.post("/documents/{document_id}/ingest")
def ingest_existing_document(
    document_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document.chunked = True
    try:
        document.chunks_count = ingest_document(document, get_settings())
        document.embedded = True
    except Exception as exc:
        document.embedded = False
        session.add(document)
        session.commit()
        raise HTTPException(
            status_code=502,
            detail=f"Document chunked, but embedding failed: {exc}",
        ) from exc
    session.add(document)
    session.commit()
    session.refresh(document)
    return document_to_dict(document)


@router.get("/plan")
def read_plan(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    return curriculum_by_week(session)


@router.post("/plan/generate")
def generate_plan(payload: PlanGenerateRequest) -> dict[str, object]:
    try:
        generated = CoachService(get_settings()).generate_plan(payload.goal, "", 42)
        return {"generated": generated, "rag_available": True}
    except Exception as exc:
        return {
            "generated": "RAG is not configured yet. Use the seeded 6-week plan to start.",
            "rag_available": False,
            "error": str(exc),
        }


@router.get("/today")
def read_today(session: Session = Depends(get_session)) -> dict[str, object]:
    today = date.today()
    active = session.scalar(
        select(PracticeSession)
        .where(PracticeSession.date == today)
        .order_by(PracticeSession.id.desc())
    )
    problem = None
    if active is not None:
        problem = active.problem
    if problem is None:
        day_number = ((today.toordinal() - 1) % 5) + 1
        week_number = (((today.toordinal() - 1) // 5) % 6) + 1
        problem = session.scalar(
            select(Problem).where(Problem.week == week_number, Problem.day == day_number)
        )
    return {
        "date": today.isoformat(),
        "problem": {
            "id": problem.id,
            "title": problem.title,
            "pattern": problem.pattern,
            "difficulty": problem.difficulty,
            "prompt": problem.prompt,
        }
        if problem
        else None,
        "workout": {
            "warm_up": "Easy: restate the pattern signal and invariant.",
            "main": "Medium: solve the selected problem with a timer.",
            "review": "Retry due mistakes before ending the session.",
            "reflection": "Write one mistake or reusable insight.",
        },
        "session": session_to_dict(active) if active else None,
    }


@router.post("/sessions/start")
def start_session(
    payload: StartSessionRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    problem = session.get(Problem, payload.problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    practice = PracticeSession(problem_id=problem.id, status="in_progress")
    session.add(practice)
    session.commit()
    session.refresh(practice)
    return session_to_dict(practice)


@router.post("/sessions/{session_id}/finish")
def finish_session(
    session_id: int,
    payload: FinishSessionRequest,
    db: Session = Depends(get_session),
) -> dict[str, object]:
    practice = db.get(PracticeSession, session_id)
    if practice is None:
        raise HTTPException(status_code=404, detail="Session not found")
    practice.status = payload.status
    practice.time_spent_mins = payload.time_spent_mins
    practice.notes = payload.notes
    practice.hint_level_used = payload.hint_level_used
    practice.review_due = next_review_date(payload.status, payload.hint_level_used, practice.date)
    practice.finished_at = utc_now()

    if payload.status == "failed":
        weak = db.scalar(select(WeakPattern).where(WeakPattern.pattern == practice.problem.pattern))
        if weak is None:
            weak = WeakPattern(pattern=practice.problem.pattern)
        weak.failures += 1
        weak.is_weak = weak.failures >= 2
        weak.updated_at = utc_now()
        db.add(weak)

    streak = db.get(Streak, 1) or Streak(id=1)
    if payload.status == "solved":
        if streak.last_active_date != practice.date:
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_active_date = practice.date
    db.add(streak)
    db.add(practice)
    db.commit()
    db.refresh(practice)
    return session_to_dict(practice)


@router.post("/hints")
def generate_hint(payload: HintRequest, session: Session = Depends(get_session)) -> dict[str, object]:
    problem_text = payload.problem
    if payload.problem_id:
        problem = session.get(Problem, payload.problem_id)
        if problem:
            problem_text = f"{problem.title}\n{problem.prompt}\nPattern: {problem.pattern}"

    try:
        hint = CoachService(get_settings()).generate_hint(
            problem_text,
            payload.current_attempt,
            payload.level,
            unlock_solution=payload.unlock_solution,
        )
        return {"hint": hint, "level": payload.level, "rag_available": True}
    except Exception as exc:
        fallback = {
            1: "think pattern signal",
            2: "Use the identified pattern and write the invariant before coding.",
            3: "Pseudocode: define state, iterate choices, update answer, review edge cases.",
        }[payload.level]
        return {
            "hint": fallback,
            "level": payload.level,
            "rag_available": False,
            "error": str(exc),
        }


@router.get("/review")
def read_review(session: Session = Depends(get_session)) -> dict[str, object]:
    due_sessions = session.scalars(
        select(PracticeSession).where(
            PracticeSession.review_due.is_not(None),
            PracticeSession.review_due <= date.today(),
        )
    ).all()
    weak = session.scalars(select(WeakPattern).order_by(WeakPattern.failures.desc())).all()
    return {
        "due_sessions": [session_to_dict(item) for item in due_sessions],
        "weak_patterns": [weak_pattern_to_dict(item) for item in weak],
    }


@router.get("/stats")
def read_stats(session: Session = Depends(get_session)) -> dict[str, object]:
    streak = session.get(Streak, 1) or Streak(id=1)
    total_sessions = session.scalar(select(func.count()).select_from(PracticeSession)) or 0
    solved = (
        session.scalar(
            select(func.count())
            .select_from(PracticeSession)
            .where(PracticeSession.status == "solved")
        )
        or 0
    )
    documents = session.scalar(select(func.count()).select_from(Document)) or 0
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "total_sessions": total_sessions,
        "solved_sessions": solved,
        "documents": documents,
    }


@router.get("/settings")
def read_settings(session: Session = Depends(get_session)) -> dict[str, object]:
    settings = get_settings()
    rows = session.scalars(select(AppSetting).order_by(AppSetting.key)).all()
    return {
        "runtime": {
            "ollama_base_url": settings.openai_base_url,
            "llm_model": settings.llm_model,
            "embedding_model": settings.embedding_model,
            "chroma_path": settings.chroma_path,
        },
        "preferences": {row.key: row.value for row in rows},
    }


@router.put("/settings")
def update_settings(
    payload: SettingsPayload,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    values = payload.model_dump(exclude_none=True)
    for key, value in values.items():
        row = session.scalar(select(AppSetting).where(AppSetting.key == key))
        if row is None:
            row = AppSetting(key=key, value=value)
        else:
            row.value = value
            row.updated_at = utc_now()
        session.add(row)
    session.commit()
    return read_settings(session)
