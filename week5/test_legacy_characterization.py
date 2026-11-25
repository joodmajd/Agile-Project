"""Characterize the legacy fee calculation before implementing its refactor."""

import pytest
from legacy_fees import calc


def legacy_courses(*hours):
    """Build the dictionary course objects expected by the original function."""
    return [{"h": hour} for hour in hours]


@pytest.mark.parametrize(
    ("hours", "kind", "summer", "expected"),
    [
        ((3, 3, 3), 1, False, 3150),
        ((3, 3, 3, 3, 3, 3), 1, True, 6250),
        ((3, 4), 2, False, 1225),
        ((3, 3), 3, True, 150),
    ],
)
def test_legacy_fee_examples_are_recorded(hours, kind, summer, expected):
    actual = calc(legacy_courses(*hours), kind, 2026, summer, None)

    assert actual == expected
