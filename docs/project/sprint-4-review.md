# Sprint 4 review — Week 11

- Sprint dates: Week 11 (completed 25/11/2026)
- Sprint goal: Ship fixes and changes selected from user feedback; release `v1.0` (`docs/project/backlog.md`).
- Changes made from user feedback: See `docs/project/feedback.md`
- Stories planned / accepted: Sprint 4 polish, test docstrings (`10.00/10` Pylint), and `v1.0` release
- PO decision per story: Accepted by PO (Ahmed Hazem)
- CI, lint, test and BDD result: `python -m pytest -q` (43 passed), `python -m ruff check .` (All checks passed!), `python -m pylint app.py server.py quiz_bank tests week5/fees.py` (10.00/10), `.github/workflows/ci.yml`
- Release tag: `v1.0` — `https://github.com/joodmajd/Agile-Project/releases/tag/v1.0` (25/11/2026)
- Docker/free host: `docker compose up --build` (port `4173`) or `python server.py` (`http://localhost:4173`)
- Jira burndown/velocity evidence: `https://joodmajd.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog`

## Review outcome

Release `v1.0` is tagged and verified: all 43 unit/integration/BDD tests pass, `ruff check .` is clean, and `pylint` scores `10.00/10`. Ready for Week 12 live demo.
