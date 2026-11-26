# Pair-programming reflection

- **Date and duration:** 25/11/2026 (~40 minutes, swapping roles after 20 minutes)
- **Partner(s):** Ahmed Hazem and Joud Mouzad
- **Driver:** Ahmed Hazem (first 20 minutes on `quiz_bank/domain.py` and `tests/test_domain.py`), then Joud Mouzad (next 20 minutes on `tests/test_app.py` and verification)
- **Navigator:** Joud Mouzad (first 20 minutes), then Ahmed Hazem (next 20 minutes)
- **Problem examined:** Ensuring the Practice Quiz Bank (idea #5) enforces its key rules—only published questions appear in quizzes, a 10-question quiz never repeats a question, scores round half-up to the nearest whole percent, and completed attempts preserve their original course and week topic in history.
- **Test-first or characterization step:** Ran `pytest` on `tests/test_domain.py` and `tests/test_app.py` first, confirming that `test_only_published_questions_for_requested_topic_are_eligible`, `test_quiz_has_ten_unique_questions_and_excludes_drafts`, and `test_quiz_requires_all_answers_and_records_the_original_topic` passed and protected the core rules.
- **Refactoring decision:** Kept domain rules pure inside `quiz_bank/domain.py` separate from Flask routes in `app.py` and SQLite persistence in `quiz_bank/repository.py`, and added clear docstrings across the test suite so static analysis stays clean.
- **Review and verification:** Verified all 43 tests and linters with `python -m pytest -q`, `python -m ruff check .`, and `python -m pylint app.py server.py quiz_bank tests week5/fees.py` (10.00/10).
- **What I learned:** Having the Navigator watch edge cases (such as excluding draft questions and checking topic history) while the Driver focuses on code keeps the Practice Quiz Bank rules reliable.
- **What we would improve next time:** Commit small increments after each passing TDD cycle instead of batching changes at the end of the session.
