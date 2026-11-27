# Before/after comparison and pair reflection

## Measurements

| Measure | Before: `legacy_fees.py` | After: `fees.py` / kata |
|---|---:|---:|
| Ruff findings on fee source | 17 | 0 for the active project check; the frozen legacy baseline is separately preserved and reported. |
| Pylint score on fee source | 4.86/10 | 10.00/10 |
| Highest fee-function cyclomatic complexity | 9 (`calc`) | 4 (`tuition_fee`) |
| Arguments to main calculation | 6 | 5 (`extra_fees` is an immutable optional tuple) |
| Whole project tests | 16 baseline grade/legacy characterization checks before fees implementation | 27 passed after refactor |
| Letter-grade line coverage | Not measured in the starter | 100% (12 tests) |
| Fee module line coverage | Not measured in the starter | 100% |
| Test without writing invoice/output files | Not supported by the legacy calculation | Fee calculation is pure; reporting returns text and can be tested without file output. |

Raw reports are in `before.txt` and `after.txt`. The final `ruff check .` deliberately ignores the unchanged legacy baseline file; the before report runs Ruff directly against that source so the original problems remain visible.

## Pair-programming reflection

On 25/11/2026, Ahmed Hazem drove while Joud Mouzad navigated and reviewed `quiz_bank/domain.py`, `tests/test_domain.py`, and `week5/fees.py`, and we swapped roles after 20 minutes. We ran `pytest` first to verify the Practice Quiz Bank rules (only published questions in quizzes, 10 unique questions, and whole-percent rounding) and the `week5` characterization tests, then cleaned up test docstrings and verified everything with `pytest`, `ruff check .`, and `pylint app.py server.py quiz_bank tests week5/fees.py`. We learned that pairing with tests first catches edge cases in quiz scoring and topic filtering early, and next time we would commit after each individual TDD cycle.
