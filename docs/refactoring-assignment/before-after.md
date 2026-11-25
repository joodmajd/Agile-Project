# Before and after

## Before

- The browser-side application, business rules, local HTTP server, and unit tests were JavaScript.
- Ruff and Pylint could not analyze the project's code because they are Python tools.
- Quiz history used the course and week currently visible in the page at submission time. Changing a topic after starting a quiz could label an attempt with the wrong topic.
- Demo data lived in browser local storage and did not survive clearing that browser's storage.

## After

- The site is served by Flask. Quiz selection, review transitions, scoring, validation, and persistence are implemented in Python.
- Questions, quiz-session snapshots, and attempts are stored in SQLite. The quiz session keeps the original course/week and question snapshot through submission.
- The pages are server-rendered HTML with the existing CSS design; there is no JavaScript application code.
- Python unit, route, and acceptance tests run with pytest. Ruff and Pylint are configured locally and in GitHub Actions.
- The half-percent scoring boundary uses half-up rounding, matching the requirement to round to the nearest whole percent.

## Verification evidence

See `static-analysis-report.md` for the commands and results run against this version.

## Scope note

This conversion is the team's existing project adapted to Python. It does not automatically replace the instructor's provided Lab 7 Python Kata if Assignment 4 requires that specific starter code.
