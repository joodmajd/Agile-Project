"""Small, testable tuition-fee rules that replace the legacy fee script."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict

FEE_PER_HOUR = 350
STAFF_CHILD_RATE = FEE_PER_HOUR * 0.5
SCHOLARSHIP_RATE = 0
HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_FEE = 150


class StudentType(IntEnum):
    """Supported tuition categories, represented by the original type codes."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


@dataclass(frozen=True)
class Course:
    """A course contributes its credit-hour count to a fee calculation."""

    hours: int


class StudentRecord(TypedDict):
    """Fields used by the batch fee calculation."""

    name: str
    type: StudentType | int
    courses: list[Course]
    summer: bool


FEE_RATES = {
    StudentType.REGULAR: FEE_PER_HOUR,
    StudentType.STAFF_CHILD: STAFF_CHILD_RATE,
    StudentType.SCHOLARSHIP: SCHOLARSHIP_RATE,
}
STUDENT_LABELS = {
    StudentType.REGULAR: "Student",
    StudentType.STAFF_CHILD: "Staff child",
    StudentType.SCHOLARSHIP: "Scholarship student",
}


def tuition_fee(
    courses: list[Course],
    student_type: StudentType | int,
    summer: bool = False,
    discount: float | None = None,
    extra_fees: tuple[float, ...] = (),
) -> float:
    """Calculate tuition while preserving the original fee adjustment order."""
    selected_type = StudentType(student_type)
    total = sum(FEE_RATES[selected_type] * course.hours for course in courses)

    if total > HIGH_FEE_THRESHOLD:
        total -= HIGH_FEE_REDUCTION
    if summer:
        total += SUMMER_FEE
    if discount is not None:
        total -= discount
    return total + sum(extra_fees)


def report(
    courses: list[Course],
    student_type: StudentType | int,
    summer: bool = False,
    discount: float | None = None,
) -> str:
    """Return invoice text instead of printing during fee calculation."""
    selected_type = StudentType(student_type)
    total = tuition_fee(courses, selected_type, summer, discount)
    lines = [f"{STUDENT_LABELS[selected_type]} fee: {total}"]
    if total > HIGH_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students: list[StudentRecord]) -> dict[str, float]:
    """Calculate a fee for each student category, including scholarships."""
    fees: dict[str, float] = {}
    for student in students:
        student_type = StudentType(student["type"])
        fees[student["name"]] = tuition_fee(
            student["courses"], student_type, student.get("summer", False)
        )
    return fees
