"""Unit tests for the quiz-bank business rules."""

import random

import pytest

from quiz_bank.domain import (
    QuizBankError,
    create_quiz,
    published_for_topic,
    review_question,
    score_quiz,
    validate_question,
)
from quiz_bank.repository import seed_questions


def test_only_published_questions_for_requested_topic_are_eligible():
    questions = seed_questions()

    eligible = published_for_topic(questions, "SET312", 6)

    assert len(eligible) == 12
    assert all(question.status == "published" for question in eligible)
    assert all(question.week == 6 for question in eligible)


def test_quiz_has_ten_unique_questions_and_excludes_drafts():
    questions = seed_questions()

    quiz = create_quiz(questions, "SET312", 6, rng=random.Random(10))

    assert len(quiz) == 10
    assert len({question.id for question in quiz}) == 10
    assert all(question.status == "published" for question in quiz)


def test_quiz_reports_when_topic_has_too_few_published_questions():
    with pytest.raises(QuizBankError, match="at least 10"):
        create_quiz(seed_questions()[:9], "SET312", 6)


def test_score_rounds_half_up_to_whole_percent():
    questions = seed_questions()[:8]
    answers = {
        question.id: (0 if index == 0 else 1)
        for index, question in enumerate(questions)
    }

    score = score_quiz(questions, answers)

    assert score.correct == 1
    assert score.total == 8
    assert score.percent == 13


def test_review_workflow_requires_approval_before_publication():
    question = seed_questions()[-1]

    approved = review_question(question, "Instructor", "approve")
    published = review_question(approved, "Instructor", "publish")

    assert approved.status == "approved"
    assert published.status == "published"
    with pytest.raises(QuizBankError, match="Approve a question"):
        review_question(question, "Instructor", "publish")


def test_rejection_requires_feedback_and_keeps_the_note():
    question = seed_questions()[-1]

    with pytest.raises(QuizBankError, match="Add feedback"):
        review_question(question, "Instructor", "reject")
    rejected = review_question(question, "Instructor", "reject", "  Clarify it.  ")

    assert rejected.status == "rejected"
    assert rejected.review_note == "Clarify it."


def test_question_validation_rejects_missing_options():
    question = seed_questions()[-1]
    invalid_question = question.__class__(
        **{**question.__dict__, "options": ("Only one",)}
    )

    with pytest.raises(QuizBankError, match="all four"):
        validate_question(invalid_question)
