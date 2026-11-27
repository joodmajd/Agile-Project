# Sprint 2 review — Week 9

- Sprint dates: Week 9
- Sprint goal: Complete question review/publishing and start the student quiz flow (`docs/project/backlog.md`).
- Demoed increment: Instructor approve/reject/publish workflow (`US05–US08`) and student 10-question quiz generation (`US09–US10`).
- Stories planned / accepted: `US05–US10` (17 points) / `US05–US10` (17 points)
- PO decision per story: `US05–US10` accepted by PO (Seif Sobhy)
- Five Gherkin scenarios passing: `pytest` (`tests/test_bdd_scenarios.py` — 5/5 scenarios in `features/practice_quiz.feature` passing), `.github/workflows/ci.yml`
- Docker/free-host deployment: `docker compose up --build` (port `4173`) or `python server.py` (`http://localhost:4173`)
- Jira burndown/velocity evidence: `https://joodmajd.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog`
- TA feedback and follow-up issues: `[TA feedback]`

## Review outcome

Review/publishing workflow and 5 Gherkin BDD scenarios pass in CI; app runs cleanly locally and via Docker. Next: complete quiz answering, scoring, history, and user validation in Sprint 3.
