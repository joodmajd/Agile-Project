"""Application factory for the Practice Quiz Bank web app."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from quiz_bank.repository import QuizRepository
from quiz_bank.routes import quiz_bank_routes

PROJECT_ROOT = Path(__file__).resolve().parent


def create_app(test_config: dict | None = None) -> Flask:
    """Create a configured Flask app and its SQLite repository."""
    application = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "templates"),
        static_folder=str(PROJECT_ROOT / "static"),
    )
    application.config.from_mapping(
        SECRET_KEY=os.environ.get(
            "SECRET_KEY", "local-demo-key-change-before-deployment"
        ),
        DATABASE=str(PROJECT_ROOT / "instance" / "quiz_bank.sqlite3"),
    )
    if test_config:
        application.config.update(test_config)

    database_path = Path(application.config["DATABASE"])
    database_path.parent.mkdir(parents=True, exist_ok=True)
    application.extensions["quiz_repository"] = QuizRepository(database_path)
    application.register_blueprint(quiz_bank_routes)
    return application


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "4173")), debug=False)
