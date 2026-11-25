"""Integration tests for the server-rendered Flask app."""


def test_role_pages_and_role_protection(client):
    response = client.post("/questions", data={"prompt": "Should not save"})
    assert response.status_code == 302
    assert b"Switch to the Question author" in client.get("/").data

    client.post("/role", data={"role": "ta"})
    assert b"Write a question" in client.get("/").data


def test_question_is_saved_as_draft_then_approved_and_published(client, app):
    client.post("/role", data={"role": "ta"})
    client.post(
        "/questions",
        data={
            "course": "SET312",
            "week": "6",
            "prompt": "Which answer is correct?",
            "a": "Correct",
            "b": "Wrong one",
            "c": "Wrong two",
            "d": "Wrong three",
            "answer": "0",
            "explanation": "The first option is correct.",
        },
    )
    repository = app.extensions["quiz_repository"]
    added = next(
        question
        for question in repository.all_questions()
        if question.prompt == "Which answer is correct?"
    )
    assert added.status == "draft"

    client.post("/role", data={"role": "instructor"})
    client.post(f"/questions/{added.id}/review", data={"decision": "approve"})
    client.post(f"/questions/{added.id}/review", data={"decision": "publish"})

    assert repository.get_question(added.id).status == "published"


def test_quiz_requires_all_answers_and_records_the_original_topic(client, app):
    client.post("/quiz/start", data={"course": "SET312", "week": "6"})
    quiz_page = client.get("/quiz")
    assert quiz_page.status_code == 200
    assert quiz_page.data.count(b'type="radio"') == 40

    incomplete = client.post("/quiz/submit", data={})
    assert incomplete.status_code == 302
    assert client.get("/quiz").status_code == 200

    repository = app.extensions["quiz_repository"]
    quiz = repository.get_quiz_session(_active_quiz_id(client), _visitor_id(client))
    answers = {question.id: "0" for question in quiz["questions"]}
    client.post("/quiz/submit", data=answers)
    attempt = repository.attempts_for_visitor(_visitor_id(client))[0]

    assert attempt["course"] == "SET312"
    assert attempt["week"] == 6
    assert attempt["percent"] == 100
    assert b"Correct answer:" in client.get(f"/?attempt={attempt['id']}").data


def _active_quiz_id(client):
    with client.session_transaction() as browser_session:
        return browser_session["active_quiz_id"]


def _visitor_id(client):
    with client.session_transaction() as browser_session:
        return browser_session["visitor_id"]


def test_unavailable_topic_shows_a_clear_error(client):
    response = client.post(
        "/quiz/start", data={"course": "SET999", "week": "2"}, follow_redirects=True
    )

    assert b"needs at least 10 published questions" in response.data
