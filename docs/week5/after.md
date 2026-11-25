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

## Pair-programming reflection — complete after a real session

This implementation was prepared with AI assistance; no human driver/navigator session took place during this preparation, so I cannot truthfully claim role switches or partner review. Complete the following three to four sentences after pairing with a teammate:

> On [date], [driver] drove while [navigator] reviewed [specific code/test], then we switched after [time or task]. We wrote or checked [test] first and it showed [result]. We found and fixed [specific issue], then verified it with [commands]. I learned [specific learning], and next time I would [specific improvement to our pairing process].

Record actual names and events; do not leave the bracketed prompts in the submitted reflection. The course handout also asks for commits showing the real TDD cycles. This preparation did not create pair-authored commits.
