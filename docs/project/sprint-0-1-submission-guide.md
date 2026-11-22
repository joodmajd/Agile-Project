# Sprint 0 & Sprint 1: team submission guide

Use this as the team's working checklist. The named role assignments below come from the team; every meeting log, review decision, story status, PR, and test result must match what actually happened. Do not backdate or invent evidence.

## Team and standing responsibilities

**Jira team page:** [Practice Quiz Bank team](https://home.atlassian.com/o/d2990ccd-fd0b-4647-abe0-9a59207588a7/people/team/eba0286b-b957-470d-aa9b-5bccabf513d0?cloudId=d48e5e9d-71b6-411e-b58a-f8c9d4ba95fd). The team membership information here is based on the user-provided link and instruction. Use the actual Jira project/backlog or board URL on the course registration form if it differs from this team page.

| Member | Role in Sprints 0–2 | What they own | Required contribution as a developer |
|---|---|---|---|
| **Seif Sobhy** | Product Owner | Product vision, ordered backlog, story acceptance criteria, sprint goal/value, acceptance or rejection of completed stories at reviews. | Own at least one implementation/test story, raise a reviewed PR, and test another member's change. |
| **Samira Ayman** | Scrum Master | Facilitate planning, stand-ups, reviews, and retros; keep Jira states accurate; record blockers; help remove blockers; follow up the retro action. | Own at least one implementation/test story, raise a reviewed PR, and test another member's change. |
| **Joud Mouzad** | Developer | Build and integrate assigned question-authoring work; estimate and test stories; document setup as needed. | Raise a PR with code and tests; review a teammate's PR. |
| **Ahmed Hazem** | Developer | Build and integrate assigned question-review/publishing work; test the workflow and key rule. | Raise a PR with code and tests; review a teammate's PR. |

The brief counts the PO and SM as developers too. Each of the four members needs their own meaningful merged code/test contribution over the project. Coordinate a role rotation at the start of Sprint 3; the new PO and SM should be two different people.

## Sprint 0 (Week 7): setup and approval

**Suggested Sprint goal:** “Set up an approved, shared, testable starting point for Practice Quiz Bank: team, GitHub, Jira, vision, ordered backlog, and Definition of Done.” Use the exact goal your team agreed in Jira if it differs.

| Owner | Do this | Evidence to include |
|---|---|---|
| Seif — PO | Confirm idea #5 with the TA; write and prioritize the product vision/backlog; ensure each story has acceptance criteria and points; agree what belongs in the MVP. | TA-approved project choice; `vision.md`; Jira backlog link/export; story order and estimates. |
| Samira — SM | Create the Jira project/board; set Sprint 0 dates and goal; invite the instructor and TA; schedule/check ceremony records; facilitate the Sprint 0 retrospective. | Jira URL and access confirmation; Sprint 0 planning and review/retro notes; action owner and due sprint. |
| Joud — Developer | Check the shared repo structure and clean-machine README instructions; prepare the first small application setup task if needed. | GitHub repo URL; setup PR/commit that is genuinely yours; run instructions. |
| Ahmed — Developer | Check how the quiz key rule will be tested; help estimate stories and agree the Definition of Done; prepare a small test/setup task if needed. | Key-rule test plan or actual test PR; agreed DoD; estimate discussion captured in Jira. |
| Everyone | Confirm roster, GitHub usernames, role assignments, project choice, three ranked choices, and repo/Jira links on the official form. Agree the DoD together. | Completed course registration form with TA signature/approval and date. Keep student IDs on the official course form; don't add them to this public repo. |

### Sprint 0 submission checklist

- [ ] Official team registration form handed in (team of four; roles above; TA approval/signature/date; three ranked choices as required).
- [ ] Shared GitHub repo and actual Jira project/board links are in the form; instructor and TA have access to both. The team page above may not be the project board URL.
- [ ] One-paragraph product vision is committed at `docs/project/vision.md`.
- [ ] Jira backlog contains at least 15 prioritized stories, each with story points and acceptance criteria. The repo has a 16-story version at `docs/project/backlog.md`; align it with Jira.
- [ ] Team Definition of Done is agreed and committed at `docs/project/definition-of-done.md`.
- [ ] Sprint 0 review and retrospective are filled from actual events in `docs/project/sprint-0-review.md` and `docs/project/retro-0.md`.
- [ ] Submit the form and links through the course's specified channel (lab instructor/LMS); the repo alone is not the registration hand-in.

## Sprint 1 (Week 8): walking slice and CI

**Suggested Sprint goal:** “Deliver one working, reviewed question-to-practice slice and run tests plus lint automatically on every pull request.” Confirm the team's actual goal, scope, and capacity in Jira.

### Assign one story per member

At Sprint Planning, Seif selects and orders the actual Jira stories, Samira checks capacity, and the four members each take at least one small, testable story. A sensible ownership split for this product is:

| Member | Suggested Sprint 1 area | What the PR must demonstrate |
|---|---|---|
| Joud | Question authoring/tagging (choose an actual US01–US04 Jira issue) | TA can enter a question and the required fields are validated/saved as a draft; include a test. |
| Ahmed | Question review/publishing (choose an actual US05–US08 Jira issue) | Reviewer can change a question's state as specified; unpublished content stays out of student quizzes; include a state/key-rule test. |
| Samira | Student topic/quiz flow (choose an actual US09–US11 Jira issue) | Student can select the topic or start the quiz behavior covered by the story; include a test. |
| Seif | Scoring/results (choose an actual US12–US16 Jira issue) | Score/result matches the acceptance criteria; include a test. Seif still accepts/rejects stories as PO at review. |

This split is a planning suggestion, not a claim that these people already completed these stories. Use the assignments and story keys that were actually agreed in your Jira Sprint. If a story is not ready or too large, split/refine it with the PO before coding.

### What to submit for Sprint 1

- [ ] Sprint Planning record: actual goal, dates, selected Jira issue keys, capacity, estimates, and owners.
- [ ] Working increment that the TA can run from the README. Demonstrate the accepted story path; show an error/edge case too.
- [ ] One completed story per member, with acceptance criteria met and tests passing.
- [ ] A separate pull request from each member for their real code/test contribution, reviewed by a teammate and merged. Link each PR to its Jira issue. Do not split or re-label the earlier bulk project upload as four people's work.
- [ ] `.github/workflows/ci.yml` runs the tests and linter on every PR; show an actual green PR check.
- [ ] At least three short stand-up check-ins that week, logged by Samira with date, attendees, progress, next step, and blockers.
- [ ] Sprint Review: show the increment to the TA; Seif records accepted/rejected stories and reasons in `docs/project/sprint-1-review.md`.
- [ ] Sprint Retrospective: Start / Stop / Continue plus one concrete action, named owner, and due Sprint 2 in `docs/project/retro-1.md`.
- [ ] Jira burndown or velocity chart/export and CI/PR links are available for the submission/demo.

## Ready-to-use process

1. **Before coding:** Samira opens Sprint Planning; Seif states the goal and story order; team checks capacity and dependencies in Jira.
2. **During the week:** each member moves their own issue on the board, opens a small PR early, adds/updates tests, and asks a teammate to review. Samira logs three check-ins and blockers.
3. **At the end:** demonstrate the running increment; Seif accepts/rejects each done story against its acceptance criteria; Samira runs Start/Stop/Continue and records the next action.
4. **Submit evidence:** course form for Sprint 0; repo/Jira links, completed sprint records, actual PR/check URLs, and chart/export for Sprint 1. Follow the course's hand-in instructions for file format and destination.

## Important checks before hand-in

- The screenshot-aligned backlog lists 16 stories whose displayed points sum to **43**, although its reference image shows **52**. Compare against your actual Jira estimates and make the document/Jira consistent; don't silently change estimates.
- The GitHub repository is public. Do not commit student IDs, private contact details, or confidential peer evaluations.
- The current repo has the app, tests, CI workflow, and templates, but those files alone do not prove each member's work or that meetings/reviews happened. The visible repo history currently has the original README commit and one bulk project-add commit. Link the actual per-member PRs/meeting records if they exist; otherwise ask your TA how to handle missing historical evidence rather than fabricating it.
- The Jira team page was provided, but it could not be opened in this session and no project/backlog URL or board contents were provided. This guide does not claim to inspect or update Jira issues, sprint dates, or membership beyond the team's stated assumption.
