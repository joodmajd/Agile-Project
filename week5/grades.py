"""Convert numeric course scores to letter grades."""

MIN_SCORE = 0
MAX_SCORE = 100
GRADE_THRESHOLDS = ((90, "A"), (80, "B"), (70, "C"), (60, "D"))


def letter_grade(score: int) -> str:
    """Return the letter grade for a score from zero through one hundred."""
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError("Score must be between 0 and 100")

    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"
