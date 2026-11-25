# Static analysis and test report

## Environment

- Python: 3.14.6 (local verification)
- Ruff: 0.17.6
- Pylint: 4.1.4
- Pytest: 9.2.0
- Flask: 3.1.3

## Commands and results

| Command | Result |
|---|---|
| `python -m ruff check .` | Passed: all checks passed. |
| `python -m pylint app.py server.py quiz_bank` | Passed: 10.00/10. |
| `python -m pytest -q` | Passed: 16 tests. |

The tests include seven business-rule tests, four Flask route tests, and five acceptance scenarios mapped from `features/practice_quiz.feature`.

## Ruff and Pylint findings addressed

The initial analysis identified long lines and import ordering, a route factory that contained too many statements, an overly long helper signature, and a data model with many fields. Imports and formatting were corrected, route handling was moved into a Flask blueprint, attempt creation was extracted into a focused helper, and Ruff/Pylint were configured for the project's data model. The final report above reflects the clean run after those changes.

## Limits

The local run used Python 3.14.6; GitHub Actions is configured for Python 3.12. The course-supplied Lab 7 invoice Kata remains a separate project if the assignment requires that exact starter code.
