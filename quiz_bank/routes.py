"""HTTP routes for the Practice Quiz Bank."""

from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from quiz_bank.domain import (
    QUIZ_SIZE,
    Question,
    QuizBankError,
    create_quiz,
    review_question,
    score_quiz,
    validate_question,
)
from quiz_bank.repository import QuizRepository

quiz_bank_routes = Blueprint("quiz_bank", __name__)


def _repository() -> QuizRepository:
    return current_app.extensions["quiz_repository"]


def _visitor_id() -> str:
    if "visitor_id" not in session:
        session["visitor_id"] = secrets.token_urlsafe(18)
    return str(session["visitor_id"])


def _current_role() -> str:
    role = session.get("role", "student")
    return role if role in {"student", "ta", "instructor"} else "student"


@quiz_bank_routes.get("/")
def index():
    """Render the dashboard for the selected demo role."""
    repository = _repository()
    visitor = _visitor_id()
    questions = repository.all_questions()
    published_count = sum(question.status == "published" for question in questions)
    review_questions = [
        question for question in questions if question.status in {"draft", "approved"}
    ]
    rejected_questions = [
        question for question in questions if question.status == "rejected"
    ]
    result = None
    attempt_id = request.args.get("attempt")
    if attempt_id:
        result = repository.get_attempt(attempt_id, visitor)
    return render_template(
        "index.html",
        role=_current_role(),
        published_count=published_count,
        review_count=len(review_questions),
        review_questions=review_questions,
        rejected_questions=rejected_questions,
        history=repository.attempts_for_visitor(visitor),
        result=result,
        quiz_size=QUIZ_SIZE,
    )


@quiz_bank_routes.post("/role")
def change_role():
    """Change the local demonstration role."""
    role = request.form.get("role", "student")
    if role not in {"student", "ta", "instructor"}:
        flash("Choose a valid demo role.", "bad")
    else:
        session["role"] = role
        flash(f"Demo role changed to {role}.", "good")
    return redirect(url_for("quiz_bank.index"))


@quiz_bank_routes.post("/reset")
def reset_demo():
    """Restore the invented data set."""
    _repository().reset()
    session.pop("active_quiz_id", None)
    flash("Demo data reset to the invented sample questions.", "good")
    return redirect(url_for("quiz_bank.index"))


@quiz_bank_routes.post("/questions")
def add_question():
    """Validate a TA question and save it as a draft."""
    if _current_role() != "ta":
        flash("Switch to the Question author (TA) demo role first.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="authoring"))
    form = request.form
    try:
        question = Question(
            id=f"q-{uuid.uuid4().hex}",
            course=form.get("course", "").strip(),
            week=int(form.get("week", "0")),
            prompt=form.get("prompt", "").strip(),
            options=tuple(form.get(key, "").strip() for key in "abcd"),
            answer=int(form.get("answer", "-1")),
            explanation=form.get("explanation", "").strip(),
            status="draft",
            author="Demo TA",
        )
        validate_question(question)
        _repository().add_question(question)
    except (ValueError, QuizBankError) as error:
        flash(str(error) or "Week and answer must be valid numbers.", "bad")
    else:
        flash("Question saved as a draft for instructor review.", "good")
    return redirect(url_for("quiz_bank.index", _anchor="authoring"))


@quiz_bank_routes.post("/questions/<question_id>/review")
def review(question_id: str):
    """Apply a valid instructor decision to a question."""
    if _current_role() != "instructor":
        flash("Switch to the Reviewer (instructor) demo role first.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="authoring"))
    repository = _repository()
    question = repository.get_question(question_id)
    if question is None:
        flash("Question not found.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="authoring"))
    try:
        updated = review_question(
            question,
            "Demo Instructor",
            request.form.get("decision", ""),
            request.form.get("note", ""),
        )
        repository.update_question(updated)
    except QuizBankError as error:
        flash(str(error), "bad")
    else:
        flash(f"Question {updated.status}.", "good")
    return redirect(url_for("quiz_bank.index", _anchor="authoring"))


@quiz_bank_routes.post("/quiz/start")
def start_quiz():
    """Select questions and persist a snapshot for this browser session."""
    course = request.form.get("course", "").strip()
    try:
        week = int(request.form.get("week", "0"))
        selected = create_quiz(_repository().all_questions(), course, week)
    except (ValueError, QuizBankError) as error:
        flash(str(error) or "Enter a valid week number.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="practice"))

    quiz_id = uuid.uuid4().hex
    _repository().create_quiz_session(quiz_id, _visitor_id(), course, week, selected)
    session["active_quiz_id"] = quiz_id
    return redirect(url_for("quiz_bank.take_quiz"))


@quiz_bank_routes.get("/quiz")
def take_quiz():
    """Render the active quiz saved for this browser."""
    repository = _repository()
    quiz_id = session.get("active_quiz_id")
    quiz_session = (
        repository.get_quiz_session(quiz_id, _visitor_id()) if quiz_id else None
    )
    if quiz_session is None:
        flash("Create a quiz before opening the quiz page.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="practice"))
    published_count = sum(
        question.status == "published" for question in repository.all_questions()
    )
    return render_template(
        "quiz.html",
        quiz=quiz_session,
        role=_current_role(),
        published_count=published_count,
    )


@quiz_bank_routes.post("/quiz/submit")
def submit_quiz():
    """Validate answers, score them, and store an attempt."""
    repository = _repository()
    quiz_id = session.get("active_quiz_id")
    quiz_session = (
        repository.get_quiz_session(quiz_id, _visitor_id()) if quiz_id else None
    )
    if quiz_session is None:
        flash("This quiz has expired. Please create a new one.", "bad")
        return redirect(url_for("quiz_bank.index", _anchor="practice"))

    questions = quiz_session["questions"]
    try:
        answers = {
            question.id: int(request.form[question.id]) for question in questions
        }
    except (KeyError, ValueError):
        flash("Answer every question before submitting.", "bad")
        return redirect(url_for("quiz_bank.take_quiz"))

    score = score_quiz(questions, answers)
    attempt_id = uuid.uuid4().hex
    attempt = _build_attempt(attempt_id, _visitor_id(), quiz_session, answers, score)
    repository.save_attempt(attempt)
    repository.complete_quiz_session(quiz_id)
    session.pop("active_quiz_id", None)
    return redirect(url_for("quiz_bank.index", attempt=attempt_id, _anchor="practice"))


def _build_attempt(attempt_id, visitor, quiz_session, answers, score):
    """Build a history record with enough detail to show explanations."""
    return {
        "id": attempt_id,
        "visitor_id": visitor,
        "course": quiz_session["course"],
        "week": quiz_session["week"],
        "correct": score.correct,
        "total": score.total,
        "percent": score.percent,
        "at": datetime.now(UTC).isoformat(timespec="seconds"),
        "details": [
            {
                "question_id": question.id,
                "prompt": question.prompt,
                "answer": answers[question.id],
                "correct_answer": question.answer,
                "correct_option": question.options[question.answer],
                "explanation": question.explanation,
            }
            for question in quiz_session["questions"]
        ],
    }
