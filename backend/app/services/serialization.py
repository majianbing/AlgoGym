from app.models import Document, PracticeSession, Problem, WeakPattern


def problem_to_dict(problem: Problem) -> dict[str, object]:
    return {
        "id": problem.id,
        "title": problem.title,
        "leetcode_url": problem.leetcode_url,
        "pattern": problem.pattern,
        "difficulty": problem.difficulty,
        "week": problem.week,
        "day": problem.day,
        "prompt": problem.prompt,
    }


def session_to_dict(session: PracticeSession) -> dict[str, object]:
    return {
        "id": session.id,
        "date": session.date.isoformat(),
        "problem_id": session.problem_id,
        "status": session.status,
        "time_spent_mins": session.time_spent_mins,
        "notes": session.notes,
        "hint_level_used": session.hint_level_used,
        "review_due": session.review_due.isoformat() if session.review_due else None,
        "problem": problem_to_dict(session.problem) if session.problem else None,
    }


def document_to_dict(document: Document) -> dict[str, object]:
    return {
        "id": document.id,
        "filename": document.filename,
        "chunked": document.chunked,
        "embedded": document.embedded,
        "chunks_count": document.chunks_count,
        "created_at": document.created_at.isoformat(),
    }


def weak_pattern_to_dict(pattern: WeakPattern) -> dict[str, object]:
    return {
        "pattern": pattern.pattern,
        "failures": pattern.failures,
        "is_weak": pattern.is_weak,
    }
