"""Boundary and error tests for the letter-grade kata."""

import pytest
from grades import letter_grade


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0, "F"),
        (59, "F"),
        (60, "D"),
        (69, "D"),
        (70, "C"),
        (79, "C"),
        (80, "B"),
        (89, "B"),
        (90, "A"),
        (100, "A"),
    ],
)
def test_letter_grade_boundaries(score, expected):
    assert letter_grade(score) == expected


@pytest.mark.parametrize("score", [-1, 101])
def test_letter_grade_rejects_scores_outside_range(score):
    with pytest.raises(ValueError, match="between 0 and 100"):
        letter_grade(score)
