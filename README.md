# Practice Quiz Bank

A small server-rendered Python website for the SET 312 Agile Software Engineering team brief (idea #5). It demonstrates TA question authoring, instructor review and publishing, random ten-question student quizzes, whole-percent scoring, explanations, and attempt history. All bundled questions are invented.

## Requirements

- Python 3.11 or later
- Dependencies in `requirements.txt`
- Optional Docker for a container run

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Open [http://localhost:4173](http://localhost:4173). The app uses a local SQLite database in `instance/quiz_bank.sqlite3`. Select the demo role in the header to explore student, TA, and instructor workflows. The role selector is for demonstration only; it is not authentication or a security boundary. Do not use real student records.

For macOS or Linux, activate the virtual environment with `source .venv/bin/activate` and run the same Python commands.

## Run tests and code-quality checks

```powershell
python -m pip install -r requirements-dev.txt
pytest
ruff check .
pylint app.py server.py quiz_bank
```

`tests/test_domain.py` covers question selection, review, validation, and scoring. `tests/test_app.py` covers HTTP flows and saved history. `tests/test_bdd_scenarios.py` runs the five acceptance scenarios documented in `features/practice_quiz.feature`.

## Docker

```sh
docker compose up --build
```

Open [http://localhost:4173](http://localhost:4173). To retain the SQLite database between container rebuilds, mount a volume for `/app/instance` before using this beyond a disposable demonstration.

## Repository map

```text
app.py                      Flask routes and request handling
quiz_bank/domain.py         Python business rules
quiz_bank/repository.py     SQLite storage and invented seed data
templates/                  Server-rendered HTML templates
static/styles.css           Browser presentation
tests/                      Unit, route, and acceptance tests
features/                   Gherkin scenarios and their pytest mapping
docs/project/               Vision, backlog, DoD, sprint records, and demo
docs/refactoring-assignment/ Refactoring comparison and reports
```

The app stores demo attempts in SQLite. Production use would require real authentication and authorization, deployment security, user-data handling rules, backups, and a privacy review.
