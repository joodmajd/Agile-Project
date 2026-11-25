"""SQLite persistence for demo questions, quiz sessions, and attempts."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Any

from quiz_bank.domain import Question


def seed_questions() -> list[Question]:
    """Return invented demo questions for SET312 Week 6."""
    prompts = [
        (
            "What is the main purpose of a unit test?",
            "Check one small unit of behavior in isolation",
            "Deploy the complete system",
            "Replace code review",
            "Measure network speed",
            "A unit test checks a small unit of behavior, "
            "usually without external services.",
        ),
        (
            "In TDD, which step comes first?",
            "Write a failing test",
            "Refactor the whole system",
            "Deploy to production",
            "Write the final documentation",
            "The red step starts with a test that fails for behavior "
            "not implemented yet.",
        ),
        (
            "What does a passing test after implementation represent?",
            "Green",
            "Blue",
            "Deploy",
            "Estimate",
            "Green means the smallest implementation makes the test pass.",
        ),
        (
            "What is refactoring?",
            "Improve internal design while keeping behavior passing",
            "Add unrelated features",
            "Delete all tests",
            "Change the user requirement",
            "Refactoring improves structure without changing visible behavior.",
        ),
        (
            "What does BDD emphasize?",
            "Examples in a shared, understandable language",
            "Only implementation details",
            "Database indexes",
            "Server capacity",
            "BDD uses concrete examples to agree on behavior.",
        ),
        (
            "Which keyword usually introduces a precondition in Gherkin?",
            "Given",
            "When",
            "Then",
            "And",
            "Given establishes the initial context or precondition.",
        ),
        (
            "Which Gherkin keyword describes an action?",
            "When",
            "Given",
            "Then",
            "Feature",
            "When describes the event or action under test.",
        ),
        (
            "Why use a fake clock for time-dependent rules?",
            "To make time behavior deterministic",
            "To speed up the CPU",
            "To encrypt timestamps",
            "To avoid assertions",
            "A controllable clock makes boundary cases reproducible.",
        ),
        (
            "What is an acceptance criterion?",
            "A specific condition that determines whether a story is acceptable",
            "A developer job title",
            "A code formatting rule only",
            "A deployment environment",
            "Acceptance criteria state observable conditions for accepting a story.",
        ),
        (
            "What does an automated regression test protect against?",
            "Previously working behavior breaking after a change",
            "Every possible future defect",
            "The need for user feedback",
            "All design decisions",
            "Regression tests detect changes that break previously working behavior.",
        ),
        (
            "What is a test assertion?",
            "A check that an observed result matches an expectation",
            "A sprint planning meeting",
            "A Git branch",
            "A deployment environment",
            "Assertions compare actual results with expected behavior.",
        ),
        (
            "What is the goal of continuous integration?",
            "Integrate changes frequently and get automated feedback",
            "Merge only once at the end",
            "Eliminate code review",
            "Prevent all merge conflicts",
            "CI checks integrated changes early through repeatable builds and tests.",
        ),
    ]
    return [
        Question(
            id=f"q{index:02d}",
            course="SET312",
            week=6,
            prompt=prompt,
            options=(correct, distractor_one, distractor_two, distractor_three),
            answer=0,
            explanation=explanation,
            status="published",
            author="Demo TA",
            reviewer="Demo Instructor",
        )
        for index, (
            prompt,
            correct,
            distractor_one,
            distractor_two,
            distractor_three,
            explanation,
        ) in enumerate(prompts, start=1)
    ] + [
        Question(
            id="q13",
            course="SET312",
            week=6,
            prompt=(
                "Draft example: a reviewer should check the explanation "
                "as well as the answer."
            ),
            options=(
                "True",
                "False",
                "Only for timed quizzes",
                "Only after publication",
            ),
            answer=0,
            explanation=(
                "Reviewers should verify that the explanation supports the answer."
            ),
            status="draft",
            author="Demo TA",
        )
    ]


class QuizRepository:
    """Store app records in SQLite using one database file."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Open and always close a database connection."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except sqlite3.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        """Create tables and seed a fresh database once."""
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY, course TEXT NOT NULL, week INTEGER NOT NULL,
                    prompt TEXT NOT NULL, options TEXT NOT NULL,
                    answer INTEGER NOT NULL, explanation TEXT NOT NULL,
                    status TEXT NOT NULL, author TEXT NOT NULL,
                    reviewer TEXT NOT NULL, review_note TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id TEXT PRIMARY KEY, visitor_id TEXT NOT NULL, course TEXT NOT NULL,
                    week INTEGER NOT NULL, questions TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY, visitor_id TEXT NOT NULL, course TEXT NOT NULL,
                    week INTEGER NOT NULL, correct INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percent INTEGER NOT NULL, at TEXT NOT NULL, details TEXT NOT NULL
                );
                """
            )
            existing = connection.execute("SELECT COUNT(*) FROM questions").fetchone()[
                0
            ]
            if not existing:
                self._insert_questions(connection, seed_questions())

    @staticmethod
    def _insert_questions(
        connection: sqlite3.Connection, questions: list[Question]
    ) -> None:
        connection.executemany(
            """INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    question.id,
                    question.course,
                    question.week,
                    question.prompt,
                    json.dumps(question.options),
                    question.answer,
                    question.explanation,
                    question.status,
                    question.author,
                    question.reviewer,
                    question.review_note,
                )
                for question in questions
            ],
        )

    @staticmethod
    def _question_from_row(row: sqlite3.Row) -> Question:
        return Question(
            id=row["id"],
            course=row["course"],
            week=row["week"],
            prompt=row["prompt"],
            options=tuple(json.loads(row["options"])),
            answer=row["answer"],
            explanation=row["explanation"],
            status=row["status"],
            author=row["author"],
            reviewer=row["reviewer"],
            review_note=row["review_note"],
        )

    def all_questions(self) -> list[Question]:
        """Return every question ordered by course, week, and ID."""
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM questions ORDER BY course, week, id"
            ).fetchall()
        return [self._question_from_row(row) for row in rows]

    def get_question(self, question_id: str) -> Question | None:
        """Return one question or None when its ID is unknown."""
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM questions WHERE id = ?", (question_id,)
            ).fetchone()
        return self._question_from_row(row) if row else None

    def add_question(self, question: Question) -> None:
        """Insert a new question."""
        with self.connect() as connection:
            self._insert_questions(connection, [question])

    def update_question(self, question: Question) -> None:
        """Persist a changed review state."""
        with self.connect() as connection:
            connection.execute(
                """UPDATE questions SET status = ?, reviewer = ?, review_note = ?
                   WHERE id = ?""",
                (question.status, question.reviewer, question.review_note, question.id),
            )

    def create_quiz_session(
        self,
        session_id: str,
        visitor_id: str,
        course: str,
        week: int,
        questions: list[Question],
    ) -> None:
        """Save a question snapshot so later changes cannot alter this quiz."""
        payload = [asdict(question) for question in questions]
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO quiz_sessions (id, visitor_id, course, week, questions)
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, visitor_id, course, week, json.dumps(payload)),
            )

    def get_quiz_session(
        self, session_id: str, visitor_id: str
    ) -> dict[str, Any] | None:
        """Load a quiz session only for the browser that created it."""
        with self.connect() as connection:
            row = connection.execute(
                """SELECT * FROM quiz_sessions WHERE id = ? AND visitor_id = ?
                   AND completed = 0""",
                (session_id, visitor_id),
            ).fetchone()
        if not row:
            return None
        questions = [
            Question(**{**item, "options": tuple(item["options"])})
            for item in json.loads(row["questions"])
        ]
        return {
            "id": row["id"],
            "course": row["course"],
            "week": row["week"],
            "questions": questions,
        }

    def complete_quiz_session(self, session_id: str) -> None:
        """Prevent a submitted session from being submitted a second time."""
        with self.connect() as connection:
            connection.execute(
                "UPDATE quiz_sessions SET completed = 1 WHERE id = ?", (session_id,)
            )

    def save_attempt(self, attempt: dict[str, Any]) -> None:
        """Store one completed quiz attempt."""
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    attempt["id"],
                    attempt["visitor_id"],
                    attempt["course"],
                    attempt["week"],
                    attempt["correct"],
                    attempt["total"],
                    attempt["percent"],
                    attempt["at"],
                    json.dumps(attempt["details"]),
                ),
            )

    def attempts_for_visitor(self, visitor_id: str) -> list[dict[str, Any]]:
        """Return a browser's most recent attempts first."""
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM attempts WHERE visitor_id = ? ORDER BY at DESC",
                (visitor_id,),
            ).fetchall()
        return [self._attempt_from_row(row) for row in rows]

    def get_attempt(self, attempt_id: str, visitor_id: str) -> dict[str, Any] | None:
        """Return an attempt only to its owning browser session."""
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM attempts WHERE id = ? AND visitor_id = ?",
                (attempt_id, visitor_id),
            ).fetchone()
        return self._attempt_from_row(row) if row else None

    @staticmethod
    def _attempt_from_row(row: sqlite3.Row) -> dict[str, Any]:
        attempt = dict(row)
        attempt["details"] = json.loads(attempt["details"])
        return attempt

    def reset(self) -> None:
        """Restore invented sample questions and clear attempts/sessions."""
        with self.connect() as connection:
            connection.execute("DELETE FROM attempts")
            connection.execute("DELETE FROM quiz_sessions")
            connection.execute("DELETE FROM questions")
            self._insert_questions(connection, seed_questions())
