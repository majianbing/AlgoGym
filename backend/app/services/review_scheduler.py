from datetime import date, timedelta


def next_review_date(
    status: str,
    hint_level_used: int,
    today: date | None = None,
) -> date:
    base = today or date.today()
    if status == "failed":
        return base + timedelta(days=1)
    if hint_level_used >= 2:
        return base + timedelta(days=3)
    return base + timedelta(days=7)
