from datetime import date

from app.services.review_scheduler import next_review_date


def test_failed_problem_reviews_tomorrow() -> None:
    assert next_review_date("failed", 0, date(2026, 6, 28)) == date(2026, 6, 29)


def test_solved_with_level_two_or_three_hint_reviews_in_three_days() -> None:
    assert next_review_date("solved", 2, date(2026, 6, 28)) == date(2026, 7, 1)
    assert next_review_date("solved", 3, date(2026, 6, 28)) == date(2026, 7, 1)


def test_solved_without_hint_reviews_in_seven_days() -> None:
    assert next_review_date("solved", 0, date(2026, 6, 28)) == date(2026, 7, 5)
