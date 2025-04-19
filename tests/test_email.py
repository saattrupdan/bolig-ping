"""Tests for the `email` module."""

import pytest

from bolig_ping.data_models import Home
from bolig_ping.email import compose_email


@pytest.mark.parametrize(
    argnames=["homes", "expected"],
    argvalues=[
        (
            [
                Home(
                    url="https://some.url",
                    address="Some address",
                    price=1000,
                    num_rooms=3,
                    size=100,
                    monthly_fee=100,
                    year=2000,
                )
            ],
            (
                "[BoligPing] Found a new home!",
                "Hi,\n\nI found a new home that you might be interested in:\n\n"
                "<a href='https://some.url'>Some address</a>\n"
                "Price: 1,000 kr.\n"
                "Number of rooms: 3\n"
                "Size: 100 m²\n"
                "Monthly fee: 100 kr./md\n"
                "Year built: 2000\n\n"
                "Have a splendid day!\n\nBest regards,\nBoligPing",
            ),
        ),
        (
            [
                Home(
                    url="https://some.url",
                    address="Some address",
                    price=1000,
                    num_rooms=3,
                    size=100,
                    monthly_fee=100,
                    year=2000,
                ),
                Home(
                    url="https://another.url",
                    address="Another address",
                    price=2000,
                    num_rooms=4,
                    size=200,
                    monthly_fee=200,
                    year=2001,
                ),
            ],
            (
                "[BoligPing] Found 2 new homes!",
                "Hi,\n\nI found some new homes that you might be interested in:\n\n"
                "<a href='https://some.url'>Some address</a>\n"
                "Price: 1,000 kr.\n"
                "Number of rooms: 3\n"
                "Size: 100 m²\n"
                "Monthly fee: 100 kr./md\n"
                "Year built: 2000\n\n"
                "<a href='https://another.url'>Another address</a>\n"
                "Price: 2,000 kr.\n"
                "Number of rooms: 4\n"
                "Size: 200 m²\n"
                "Monthly fee: 200 kr./md\n"
                "Year built: 2001\n\n"
                "Have a splendid day!\n\nBest regards,\nBoligPing",
            ),
        ),
    ],
    ids=["one_home", "two_homes"],
)
def test_compose_email(homes: list[Home], expected: str) -> None:
    """Test that an email is composed."""
    email = compose_email(homes=homes)
    assert email == expected
