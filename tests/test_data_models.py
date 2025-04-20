"""Tests for the `data_models` module."""

from collections.abc import Generator

import pytest

from bolig_ping.data_models import Home, SearchQuery


@pytest.mark.parametrize(
    argnames=["search_query", "expected"],
    argvalues=[
        (
            SearchQuery(
                cities=["københavn-n"],
                min_price=100,
                max_price=200,
                min_monthly_fee=100,
                max_monthly_fee=200,
                min_rooms=3,
                max_rooms=5,
                min_size=50,
                max_size=100,
                queries=["badekar"],
                property_type=["ejerlejlighed"],
            ),
            "https://www.boligsiden.dk/by/københavn-n/tilsalg/ejerlejlighed,"
            "villalejlighed?priceMin=100&priceMax=200&numberOfRoomsMin=3"
            "&numberOfRoomsMax=5&areaMin=50&areaMax=100",
        ),
        (
            SearchQuery(cities=["københavn-n"], min_price=100),
            "https://www.boligsiden.dk/by/københavn-n/tilsalg?priceMin=100",
        ),
        (
            SearchQuery(cities=["københavn-n"]),
            "https://www.boligsiden.dk/by/københavn-n/tilsalg",
        ),
        (
            SearchQuery(cities=["københavn-n", "brøndby"]),
            "https://www.boligsiden.dk/by/københavn-n,brøndby/tilsalg",
        ),
        (SearchQuery(), "https://www.boligsiden.dk/tilsalg"),
    ],
    ids=[
        "all-arguments",
        "city-and-min-price",
        "city-only",
        "multiple-cities",
        "no-arguments",
    ],
)
def test_get_url(search_query: SearchQuery, expected: str) -> None:
    """Test the `SearchQuery.get_url` method."""
    url = search_query.get_url()
    assert url == expected


class TestHome:
    """Tests for the `Home` data model."""

    @pytest.fixture(scope="class")
    def home(self) -> Generator[Home, None, None]:
        """Return a `Home` instance."""
        yield Home(
            url="https://some.url",
            address="Some address",
            price=1000,
            num_rooms=3,
            size=100,
            monthly_fee=100,
            year=2000,
        )

    def test_hash(self, home: Home) -> None:
        """Test the `__hash__` method."""
        assert hash(home) == hash(home.url)

    def test_to_html(self, home: Home) -> None:
        """Test the `to_html` method."""
        assert home.to_html() == (
            "<a href='https://some.url'>Some address</a>\n"
            "Price: 1,000 kr.\n"
            "Number of rooms: 3\n"
            "Size: 100 m²\n"
            "Monthly fee: 100 kr./md\n"
            "Year built: 2000"
        )

    def test_to_text(self, home: Home) -> None:
        """Test the `to_text` method."""
        assert home.to_text() == (
            "URL: https://some.url\n"
            "Address: Some address\n"
            "Price: 1,000 kr.\n"
            "Number of rooms: 3\n"
            "Size: 100 m²\n"
            "Monthly fee: 100 kr./md\n"
            "Year built: 2000"
        )
