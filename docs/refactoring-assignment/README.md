# Python refactoring assignment work

## What changed

The Practice Quiz Bank has been converted from a JavaScript-driven page to a server-rendered Python application. Flask handles requests, Python modules contain quiz rules, and SQLite stores questions, quiz snapshots, and attempts. HTML templates and CSS remain because browsers need markup and styles; the interactive app logic and tests are Python.

## Five deliverables

1. **Source code:** `app.py`, `server.py`, `quiz_bank/domain.py`, `quiz_bank/repository.py`, `templates/`, and `static/styles.css`.
2. **Tests:** `tests/test_domain.py`, `tests/test_app.py`, and `tests/test_bdd_scenarios.py`.
3. **Reports:** `static-analysis-report.md` records actual Ruff, Pylint, and pytest results.
4. **Before/after comparison:** `before-after.md` explains the migration and the topic-history bug fix.
5. **Pair-programming reflection:** `pair-programming-reflection.md` is a fill-in template for your real team session.

## Run it

See the project README for local setup, run, and check commands. GitHub Actions installs the Python development dependencies and runs Ruff, Pylint, and pytest.

## Course-submission note

This converts your Practice Quiz Bank project into Python so Ruff and Pylint can assess it. The course assignment may still require the specific Python Kata supplied in the Lab 7 ZIP. Confirm that project substitution is allowed; if the instructor requires the Kata, submit the Kata work as well.

## AI use

AI assistance was used to convert the app, add tests, configure Python tooling, and draft the technical notes. Review and understand the changes with your team and disclose AI use according to your course rules.
