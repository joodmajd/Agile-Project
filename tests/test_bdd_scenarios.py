"""Acceptance-level tests mapped to the Gherkin feature scenarios."""

import re


def test_draft_questions_are_not_available_to_students(client):
    client.post("/quiz/start", data={"course": "SET312", "week": "6"})
    response = client.get("/quiz")

    assert b"Draft example" not in response.data
    assert response.data.count(b"<fieldset>") == 10


def test_reviewer_approves_and_publishes_a_draft_question(client, app):
    repository = app.extensions["quiz_repository"]
    draft = next(
        question
        for question in repository.all_questions()
        if question.status == "draft"
    )
    client.post("/role", data={"role": "instructor"})

    client.post(f"/questions/{draft.id}/review", data={"decision": "approve"})
    client.post(f"/questions/{draft.id}/review", data={"decision": "publish"})

    assert repository.get_question(draft.id).status == "published"


def test_student_receives_ten_random_questions_without_repeats(client):
    client.post("/quiz/start", data={"course": "SET312", "week": "6"})
    response = client.get("/quiz")

    assert response.data.count(b"<fieldset>") == 10
    option_names = re.findall(rb'name="(q\d+)"', response.data)
    assert len(set(option_names)) == 10


def test_student_receives_score_and_explanations(client):
    client.post("/quiz/start", data={"course": "SET312", "week": "6"})
    with client.session_transaction() as browser_session:
        quiz_id = browser_session["active_quiz_id"]
        visitor = browser_session["visitor_id"]
    repository = client.application.extensions["quiz_repository"]
    quiz = repository.get_quiz_session(quiz_id, visitor)
    answers = {question.id: "0" for question in quiz["questions"]}
    client.post("/quiz/submit", data=answers)
    attempt = repository.attempts_for_visitor(visitor)[0]

    response = client.get(f"/?attempt={attempt['id']}")
    assert b"100%" in response.data
    assert b"Correct answer:" in response.data


def test_completed_quiz_is_saved_with_its_topic(client, app):
    client.post("/quiz/start", data={"course": "SET312", "week": "6"})
    with client.session_transaction() as browser_session:
        quiz_id = browser_session["active_quiz_id"]
        visitor = browser_session["visitor_id"]
    repository = app.extensions["quiz_repository"]
    quiz = repository.get_quiz_session(quiz_id, visitor)
    client.post(
        "/quiz/submit", data={question.id: "0" for question in quiz["questions"]}
    )

    attempt = repository.attempts_for_visitor(visitor)[0]
    assert (attempt["course"], attempt["week"]) == ("SET312", 6)
