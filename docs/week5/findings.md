# Static-analysis findings and hidden bug

## Before-refactoring lint findings

The untouched `week5/legacy_fees.py` was checked with Ruff 0.17.6 and Pylint 4.1.4. The raw outputs and commands are saved in `before.txt`.

Ruff reported **17 findings**. The handout's sample reports 16; the installed Ruff version also reports `PLR0917` (too many positional arguments), making this run's count 17.

| Ruff rule | Count | Smell | Improvement |
|---|---:|---|---|
| F401 | 2 | Dead imports | Remove unused `os` and `math`. |
| PLR2004 | 6 | Magic values / type codes | Name fee constants and use `StudentType`. |
| C901 | 1 | Complex conditional calculation | Replace the type branch with a rate table and keep one fee path. |
| PLR0913 | 1 | Too many responsibilities in one signature | Remove unused year; group the calculation around meaningful inputs. |
| PLR0917 | 1 | Too many positional arguments | Reduce inputs and give optional values safe defaults. |
| ARG001 | 1 | Unused year parameter | Remove `y`; it has no effect on the calculation. |
| B006 | 1 | Mutable list default | Use immutable `extra_fees=()`. |
| E711 / E712 | 2 | Non-idiomatic Boolean and None comparisons | Use `if summer` and `discount is not None`. |
| F841 | 1 | Dead local value | Remove unused `tmp`. |
| N802 | 1 | Inconsistent function naming | Rename `ProcessAll` to `process_all`. |

Pylint gave the legacy file **4.86/10**. Among other warnings, it specifically reported a possible use of `fee` before assignment in `ProcessAll` (`E0606`).

## Smells found by reading the code

Ruff reports patterns, but the team should also notice these design problems:

- `calc(d, t, y, s, disc, extra)` uses unclear names and mixes unrelated data types. `{"h": hours}` makes a course's shape implicit.
- `calc` calculates a fee while `report` prints, decides labels, and returns a value. Printing is a side effect that makes the function harder to reuse and test.
- The student-type conditions are duplicated in `calc` and `ProcessAll`, so the fee rules can drift apart.
- `ProcessAll` carries a local `fee` from one loop iteration to the next, coupling a student's result to the previous student's type and order.

## Hidden bug

`ProcessAll` uses two independent `if` statements for types 1 and 2. A scholarship student (type 3) matches neither, so the function never assigns a fee for that student. In the handout's order, Sara's 1050 EGP stays in the local variable and Omar is incorrectly printed as 1050 EGP; if Omar is first, Python raises `UnboundLocalError`. The refactored `process_all` converts every type to `StudentType` and calculates every student through the same rate table, so a scholarship student's tuition is correctly zero (plus any applicable summer/other adjustments).

## Improvements

- Replaced numeric student codes with `StudentType` and fee literals with named constants.
- Added an immutable `Course` data class instead of course dictionaries.
- Replaced repeated type branches with `FEE_RATES` and a single `tuition_fee` calculation.
- Removed the mutable default, unused imports/variable/year, and printing from the calculation path.
- Made `report` return its text and made `process_all` return a result mapping for all supported types.
- Added tests that compare the refactor with the original calculation, cover adjustments, and reproduce the scholarship-order regression.
