# Product vision: Practice Quiz Bank

**For** ECU students who need dependable practice before quizzes, **Practice Quiz Bank** is a course-based question bank that turns scattered practice material into short, topic-specific quizzes with explanations. **Unlike** unreviewed shared PDFs, questions follow a draft → review → published workflow so students practice from reviewed content and can revisit their topic history.

## Users and value

- **Student:** take a random ten-question practice quiz, see a score and explanations, and revisit attempt history by course/week.
- **Question author (TA):** write a multiple-choice question, assign a course and week, and save it as a draft.
- **Reviewer (instructor):** review draft content and publish or reject it before students can see it.

## MVP boundaries

The MVP delivers the four brief epics: author tagged MCQs; review and publish; random ten-question quiz with score; explanations and topic history. The business rule is enforced in the quiz domain: **only published questions are eligible; a quiz contains no repeated question; score is correct ÷ total, rounded to the nearest whole percent.**

Stretch ideas, only after all four MVP epics are stable: weak-topic recommendations, timed mode, and difficulty statistics.

## Product assumptions to validate

1. A question needs four options, exactly one correct option, and a concise explanation.
2. A useful quiz requires at least ten published questions in the selected course/week. The MVP shows a clear message when fewer are available.
3. Course and week identify the topic for filtering and history.
4. The starter runs as a local demo and stores invented sample data in the current browser. For a real multi-user deployment, the group must add server-side storage, identity, authorization, and data backup.

## Success measures for the course demo

- All four MVP epics demonstrated end to end.
- At least five Gherkin scenarios pass in the group's runner.
- Key rule unit tests and CI pass on the shared main branch.
- Three real users try the MVP; their feedback leads to a documented product/backlog change.
- All members can explain a contribution and show a reviewed merged pull request.
