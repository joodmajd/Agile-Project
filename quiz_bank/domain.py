"""Domain rules for question review, quiz selection, and scoring."""

from __future__ import annotations

import random
from dataclasses import dataclass, replace

QUIZ_SIZE = 10


class QuizBankError(ValueError):
    """Raised when a requested quiz-bank operation violates a domain rule."""


@dataclass(frozen=True)
class Question:
    """A multiple-choice question and its review state."""

    id: str
    course: str
    week: int
    prompt: str
    options: tuple[str, ...]
    answer: int
    explanation: str
    status: str = "draft"
    author: str = "Demo TA"
    reviewer: str = ""
    review_note: str = ""


@dataclass(frozen=True)
class Score:
    """The result of checking a set of answers."""

    correct: int
    total: int
    percent: int


def published_for_topic(
    questions: list[Question], course: str, week: int
) -> list[Question]:
    """Return only questions published for the requested course and week."""
    return [
        question
        for question in questions
        if question.status == "published"
        and question.course == course
        and question.week == week
    ]


def create_quiz(
    questions: list[Question],
    course: str,
    week: int,
    *,
    size: int = QUIZ_SIZE,
    rng: random.Random | None = None,
) -> list[Question]:
    """Choose a random, non-repeating quiz from a published topic pool."""
    if size < 1:
        raise QuizBankError("A quiz must contain at least one question.")

    pool = published_for_topic(questions, course, week)
    if len(pool) < size:
        raise QuizBankError(
            f"This topic needs at least {size} published questions "
            f"(currently {len(pool)})."
        )
    return (rng or random).sample(pool, size)


def score_quiz(questions: list[Question], answers: dict[str, int]) -> Score:
    """Calculate correct answers and a whole-number percentage."""
    if not questions:
        raise QuizBankError("A quiz must contain at least one question.")

    correct = sum(answers.get(question.id) == question.answer for question in questions)
    percent = int(correct / len(questions) * 100 + 0.5)
    return Score(correct, len(questions), percent)


def review_question(
    question: Question, reviewer: str, decision: str, note: str = ""
) -> Question:
    """Approve, publish, or reject a question while enforcing its workflow."""
    if question.status not in {"draft", "approved"}:
        raise QuizBankError("Only draft or approved questions can be reviewed.")
    if decision not in {"approve", "publish", "reject"}:
        raise QuizBankError("Choose approve, publish, or reject.")
    if decision == "approve" and question.status != "draft":
        raise QuizBankError("Only draft questions can be approved.")
    if decision == "publish" and question.status != "approved":
        raise QuizBankError("Approve a question before publishing it.")
    if decision == "reject" and not note.strip():
        raise QuizBankError("Add feedback when rejecting a question.")

    new_status = {
        "approve": "approved",
        "publish": "published",
        "reject": "rejected",
    }[decision]
    review_note = note.strip() if decision == "reject" else question.review_note
    return replace(
        question,
        status=new_status,
        reviewer=reviewer,
        review_note=review_note,
    )


def validate_question(question: Question) -> None:
    """Raise a useful error if a submitted multiple-choice question is invalid."""
    if not question.course.strip() or not question.prompt.strip():
        raise QuizBankError("Enter a course and question.")
    if not 1 <= question.week <= 20:
        raise QuizBankError("Week must be between 1 and 20.")
    if len(question.options) != 4 or any(
        not option.strip() for option in question.options
    ):
        raise QuizBankError("Enter all four answer options.")
    if not 0 <= question.answer < len(question.options):
        raise QuizBankError("Select a valid correct answer.")
    if not question.explanation.strip():
        raise QuizBankError("Enter an explanation.")
