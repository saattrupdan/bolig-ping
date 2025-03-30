"""Tests for the `scraper` module."""

import pytest

from bolig_ping.scraper import extract_number


@pytest.mark.parametrize(
    argnames=["text", "expected"],
    argvalues=[
        ("1.000 kr.", 1000),
        ("1.000.000 kr.", 1000000),
        ("I alt 1.000.000 kr.", 1000000),
        ("I alt\n\n1.000.000 kr.", 1000000),
    ],
    ids=["Thousands", "Millions", "With text", "With text and newlines"],
)
def test_extract_number(text: str, expected: int) -> None:
    """Test the `extract_number` function."""
    assert extract_number(text=text) == expected
