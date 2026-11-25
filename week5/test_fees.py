"""Characterization and regression tests for the refactored fee code."""

import pytest
from fees import Course, StudentType, process_all, report, tuition_fee
from legacy_fees import calc


def legacy_courses(*hours):
    """Build dictionary objects for calls to the unchanged legacy function."""
    return [{"h": hour} for hour in hours]


def courses(*hours):
    """Build domain objects for calls to the refactored function."""
    return [Course(hour) for hour in hours]


def student(name, kind):
    """Build a sample student record for the batch processor."""
    return {
        "name": name,
        "type": kind,
        "courses": courses(3),
        "summer": False,
    }


@pytest.mark.parametrize(
    ("hours", "code", "kind", "summer"),
    [
        ((3, 3, 3), 1, StudentType.REGULAR, False),
        ((3, 3, 3, 3, 3, 3), 1, StudentType.REGULAR, True),
        ((3, 4), 2, StudentType.STAFF_CHILD, False),
        ((3, 3), 3, StudentType.SCHOLARSHIP, True),
    ],
)
def test_same_result_as_legacy(hours, code, kind, summer):
    old_total = calc(legacy_courses(*hours), code, 2026, summer, None)

    new_total = tuition_fee(courses(*hours), kind, summer)

    assert new_total == old_total


def test_large_regular_fee_gets_the_original_reduction():
    assert tuition_fee(courses(6, 6, 6), StudentType.REGULAR) == 6100


def test_optional_discount_and_extra_fees_keep_the_original_order():
    old_total = calc(legacy_courses(6, 6, 6), 1, 2026, True, 100, extra=[25, 50])

    new_total = tuition_fee(
        courses(6, 6, 6),
        StudentType.REGULAR,
        summer=True,
        discount=100,
        extra_fees=(25, 50),
    )

    assert new_total == old_total == 6225


def test_scholarship_is_processed_with_zero_tuition_in_either_order():
    regular_first = [
        student("Sara", StudentType.REGULAR),
        student("Omar", StudentType.SCHOLARSHIP),
    ]
    scholarship_first = list(reversed(regular_first))

    assert process_all(regular_first) == {"Sara": 1050, "Omar": 0}
    assert process_all(scholarship_first) == {"Omar": 0, "Sara": 1050}


def test_scholarship_summer_fee_is_preserved():
    assert tuition_fee(courses(3), StudentType.SCHOLARSHIP, summer=True) == 150


def test_report_returns_text_without_printing(capsys):
    text = report(courses(6, 6, 6), StudentType.REGULAR)

    assert text == "Student fee: 6100\nHigh fee"
    assert capsys.readouterr().out == ""


def test_report_supports_scholarship_students():
    text = report(courses(3), StudentType.SCHOLARSHIP)

    assert text == "Scholarship student fee: 0"


def test_unknown_student_type_is_rejected():
    with pytest.raises(ValueError):
        tuition_fee(courses(3), 99)
