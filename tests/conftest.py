"""Shared fixtures for domain and browser-route tests."""

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """Create an isolated Flask app and SQLite database for a test."""
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE": str(tmp_path / "quiz_bank.sqlite3"),
        }
    )


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """Return a Flask test client."""
    return app.test_client()
