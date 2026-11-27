Feature: Reviewed practice quizzes
  Students practice from instructor-approved questions and learn from explanations.

  Scenario: Draft questions are hidden from students
    Given a question is in draft status
    When a student creates a quiz for its course and week
    Then the draft question is not included

  Scenario: A reviewer approves and publishes a draft question
    Given a TA has saved a valid draft question
    When the instructor approves it
    Then the question status becomes approved
    When the instructor publishes the approved question
    Then the question status becomes published
    And the question is eligible for a matching practice quiz

  Scenario: A student receives a ten question quiz without repeats
    Given at least ten published questions match the chosen course and week
    When the student starts a practice quiz
    Then exactly ten distinct questions are selected

  Scenario: A student sees the score and explanations
    Given a student answered all questions in a quiz
    When the student submits the quiz
    Then the score is correct answers divided by total and rounded to a whole percent
    And each question explanation is displayed

  Scenario: A completed quiz is recorded by topic
    Given a student completed a quiz for SET312 week 6
    When the quiz is submitted
    Then the attempt appears in the student's history for that topic
