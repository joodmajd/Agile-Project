# The 16 User Stories (with Priorities & Story Points)

This is the team's screenshot-aligned backlog: four epics, four stories each. The priority labels and points below match the rows shown in the reference image. Each story has a testable acceptance criterion to satisfy the brief's backlog requirement.

| Epic | ID | User story title | Priority | Story points | Acceptance criteria |
|---|---|---|---|---:|---|
| **1. Question Management** | US01 | Create multiple-choice questions | Highest | 3 | Given a TA enters a non-empty prompt, when saved, then a new question is created as a draft and is not visible in student quizzes. |
|  | US02 | Add answer options and select correct answer | Highest | 2 | Given a draft, when the TA supplies four non-empty options and marks one correct, then the options and answer are saved; incomplete options cannot be submitted. |
|  | US03 | Tag questions by course | High | 2 | Given a draft, when the TA selects a course code, then the course tag is saved and available for quiz filtering. |
|  | US04 | Tag questions by week | High | 2 | Given a draft, when the TA selects a valid course week, then the week tag is saved and available for quiz filtering. |
| **2. Question Review & Publishing** | US05 | View submitted questions | Highest | 2 | Given submitted drafts exist, when the instructor opens the review queue, then each draft shows prompt, options, correct answer, explanation, course, and week. |
|  | US06 | Approve questions | Highest | 2 | Given a draft passes review, when the instructor approves it, then its status becomes approved and it remains unavailable to students until published. |
|  | US07 | Reject questions with feedback | High | 3 | Given a draft or approved question needs changes, when the instructor rejects it with a reason, then it becomes rejected, stays out of quizzes, and the author can see the feedback. |
|  | US08 | Publish approved questions | Highest | 2 | Given a question is approved, when the instructor publishes it, then its status becomes published and it becomes eligible for quizzes matching its course/week. Draft, approved, and rejected questions are never quiz-eligible. |
| **3. Practice Quiz** | US09 | Select course and week | High | 3 | Given the student chooses a course and week, when a quiz starts, then only published questions with both matching tags are considered. |
|  | US10 | Generate random 10-question quiz | Highest | 5 | Given at least ten matching published questions exist, when a quiz starts, then exactly ten distinct questions are selected at random. If fewer than ten exist, the app gives a clear message and does not start a partial quiz. |
|  | US11 | Answer questions | Highest | 3 | Given an active quiz, when the student selects an option for every question, then answers are retained until submission; submission is blocked while any question is unanswered. |
|  | US12 | Calculate quiz score | Highest | 3 | Given a submitted quiz with C correct answers out of N, when the result is calculated, then the correct count and percentage `round(C ÷ N × 100)` are displayed. |
| **4. Results & History** | US13 | View correct answers and explanations | High | 3 | Given a submitted attempt, when results display, then each question shows whether the response was correct, the correct answer, and its explanation. |
|  | US14 | View previous attempts | High | 3 | Given a student has completed quizzes, when history opens, then previous attempts appear with date/time, topic, score, and question total. |
|  | US15 | View history by topic | Medium | 3 | Given attempts exist for multiple topics, when the student filters/selects a course and week, then only attempts for that topic are shown. |
|  | US16 | Display score as percentage | High | 2 | Given a completed quiz, when its result is shown in quiz results and history, then the score appears as a whole-number percentage from 0% to 100%, rounded to the nearest percent. |

## Point total check

The visible row values add to **43 points**: Question Management 9 + Review & Publishing 9 + Practice Quiz 14 + Results & History 11. The reference image's footer says **52**, which is 9 points higher than the sum of its 16 displayed stories. This pack preserves every row value from the image and corrects the total rather than changing estimates to force a match. If 52 is your Jira total, check whether nine points belong to an omitted story or whether one or more displayed estimates should change, then keep this document and Jira consistent.

## Suggested Jira keys and sprint grouping

Use the IDs above as Jira issue summaries/labels (or map them to your existing issue keys). This grouping is a suggested flow; keep the real Sprint assignments, capacity, and velocity from your Jira project as the source of truth.

| Sprint | Suggested goal | Stories | Points from this table |
|---|---|---|---:|
| Sprint 0 (Week 7) | Set up team, vision, repo, Jira, Definition of Done, and initial backlog. | Planning/setup work | 0 story points |
| Sprint 1 (Week 8) | Build the question-authoring foundation. | US01–US04 | 9 |
| Sprint 2 (Week 9) | Complete question review/publishing and start the student quiz flow. | US05–US10 | 17 |
| Sprint 3 (Week 10) | Finish quiz answering, scoring, results, and history; validate the complete MVP with users. | US11–US16 | 17 |
| Sprint 4 (Week 11) | Ship fixes and changes selected from real user feedback; release v1.0. | Reprioritized feedback issues | Re-estimate in Jira |

These allocations total the row sum of 43 and match the current Jira sprint assignments. They are a plan, not evidence of completed work or accepted velocity. Sprint 2 and Sprint 3 each total 17 points; revisit the selected scope against the team's actual capacity during sprint planning.
