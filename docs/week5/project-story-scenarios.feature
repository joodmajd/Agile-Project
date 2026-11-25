Feature: Student practices with published quiz questions
  As a student
  I want to practice a selected course topic
  So that I can check my understanding before a quiz

  Scenario: Start a quiz when enough questions are published
    Given 12 questions are published for SET312 week 6
    When I start a practice quiz for SET312 week 6
    Then I receive 10 different published questions

  Scenario: Refuse a quiz when too few questions are published
    Given 9 questions are published for SET312 week 6
    When I start a practice quiz for SET312 week 6
    Then I see a message that at least 10 published questions are required

  Scenario: Review a completed quiz
    Given I have answered all 10 questions in a SET312 week 6 quiz
    When I submit my answers
    Then I see my whole-number score and explanations
    And my attempt is saved under SET312 week 6
