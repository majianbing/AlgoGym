import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Problem


def load_seed_curriculum(session: Session) -> None:
    existing = session.scalar(select(Problem.id).limit(1))
    if existing is not None:
        return

    current = Path(__file__).resolve()
    candidates = [
        current.parents[2] / "seeds" / "curriculum.json",
        current.parents[3] / "seeds" / "curriculum.json",
    ]
    seed_path = next(path for path in candidates if path.exists())
    curriculum = json.loads(seed_path.read_text(encoding="utf-8"))
    for week in curriculum:
        for item in week["problems"]:
            prompt = (
                f"Practice {item['pattern']} with a mock {item['difficulty']} problem. "
                "Identify the pattern signal, write the invariant, solve, then review mistakes."
            )
            session.add(
                Problem(
                    title=item["title"],
                    leetcode_url="",
                    pattern=item["pattern"],
                    difficulty=item["difficulty"],
                    week=week["week"],
                    day=item["day"],
                    prompt=prompt,
                )
            )
    session.commit()


def curriculum_by_week(session: Session) -> list[dict[str, object]]:
    rows = session.scalars(select(Problem).order_by(Problem.week, Problem.day)).all()
    weeks: dict[int, list[Problem]] = {}
    for problem in rows:
        weeks.setdefault(problem.week, []).append(problem)
    return [
        {
            "week": week,
            "problems": [
                {
                    "id": problem.id,
                    "title": problem.title,
                    "pattern": problem.pattern,
                    "difficulty": problem.difficulty,
                    "day": problem.day,
                    "leetcode_url": problem.leetcode_url,
                    "prompt": problem.prompt,
                }
                for problem in problems
            ],
        }
        for week, problems in sorted(weeks.items())
    ]
