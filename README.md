# Practice Quiz Bank

A small, browser-based MVP for the SET 312 Agile Software Engineering team brief (idea #5). It demonstrates TA question authoring, instructor review and publishing, a random ten-question student quiz, whole-percent scoring, explanations, and local topic history. All bundled question content is invented.

## Requirements

- Node.js 22 or later (no runtime npm dependencies)
- Optional Docker for the container run

## Run locally

```sh
npm run serve
```

Open [http://localhost:4173](http://localhost:4173). The local app stores its demo state in this browser's `localStorage`. Use “Reset demo” to restore the original sample data. Do not use real student records or private data.

For Docker, run `docker compose up --build` and open the same URL. The sample's localStorage still belongs to the browser; Docker does not add shared server-side data storage.

## Run checks

```sh
npm run check
```

The unit tests cover the central business rule, question review workflow, scoring, and attempt history. `npm run check` also runs five executable Gherkin-mapped scenarios and JavaScript syntax checks. GitHub Actions runs ESLint as well. See `features/practice_quiz.feature` and `features/steps.md` for the behavior and runner mapping.

## Demo journey

1. Select **Question author (TA)** and submit a new question. It appears as a draft.
2. Select **Reviewer (instructor)**, approve the draft, then publish it; rejection requires feedback.
3. Select **Student**, choose SET312 / Week 6, answer all ten questions, and submit.
4. Review the score, correct answers, explanations, and recent attempt history.
5. Try a course/week with too few published questions to see the validation message.

Role selector is only a local demo aid; it does not provide authentication or security. Data is stored locally per browser and does not synchronize. Do not deploy this starter for real student use without a backend, authentication, authorization, validation, and an appropriate data policy.

## Repository map

```text
src/                         Browser app and business logic
tests/                       Node unit tests
features/                    Gherkin scenarios and mapping
.github/workflows/ci.yml     GitHub Actions test pipeline
docs/project/                Vision, backlog, DoD, sprint records, feedback, demo
```

## Team project checklist

See `docs/project/sprint-0-1-submission-guide.md` for the named team responsibilities and Sprint 0/1 hand-in checklist. The repository also includes the vision, DoD, screenshot-aligned 16-story backlog, sprint/retro templates, and feedback log. Replace templates with actual evidence before hand-in.
