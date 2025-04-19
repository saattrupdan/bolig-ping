"""Tests for the `data_models` module."""

from collections.abc import Generator

import pytest

from bolig_ping.data_models import Home, SearchQuery


class TestSearchQuery:
    """Tests for the `SearchQuery` data model."""

    @pytest.fixture(scope="class")
    def search_query(self) -> Generator[SearchQuery, None, None]:
        """Return a `SearchQuery` instance."""
        yield SearchQuery(
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
        )

    def test_create_search_query(self, search_query: SearchQuery) -> None:
        """Test creating a `SearchQuery` instance."""
        assert search_query.cities == ["københavn-n"]
        assert search_query.min_price == 100
        assert search_query.max_price == 200
        assert search_query.min_monthly_fee == 100
        assert search_query.max_monthly_fee == 200
        assert search_query.min_rooms == 3
        assert search_query.min_size == 50
        assert search_query.queries == ["badekar"]

    def test_get_url(self, search_query: SearchQuery) -> None:
        """Test the `get_url` method."""
        url = search_query.get_url()
        assert url == (
            "https://www.boligsiden.dk/by/københavn-n/tilsalg/ejerlejlighed,"
            "villalejlighed?priceMin=100&priceMax=200&numberOfRoomsMin=3"
            "&numberOfRoomsMax=5&areaMin=50&areaMax=100"
        )


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

    def test_create_home(self, home: Home) -> None:
        """Test creating a `Home` instance."""
        assert home.url == "https://some.url"
        assert home.address == "Some address"
        assert home.price == 1000
        assert home.num_rooms == 3
        assert home.size == 100
        assert home.monthly_fee == 100
        assert home.year == 2000

    def test_hash(self, home: Home) -> None:
        """Test the `__hash__` method."""
        assert hash(home) == hash(home.url)
