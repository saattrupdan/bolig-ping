"""Tests for the `cache` module."""

from collections.abc import Generator
from pathlib import Path

import pytest

from bolig_ping.cache import store_to_cache
from bolig_ping.data_models import Home


class TestStoreToCache:
    """Tests for the store_to_cache function."""

    @pytest.fixture(scope="class")
    def home(self) -> Generator[Home, None, None]:
        """Return a Home object."""
        yield Home(
            url="https://some.url",
            address="Some address",
            price=1000,
            num_rooms=3,
            size=100,
            monthly_fee=100,
            year=2000,
        )

    @pytest.fixture(scope="class")
    def another_home(self) -> Generator[Home, None, None]:
        """Return another Home object."""
        yield Home(
            url="https://another.url",
            address="Another address",
            price=2000,
            num_rooms=4,
            size=200,
            monthly_fee=200,
            year=2001,
        )

    def test_home_is_stored(self, home: Home) -> None:
        """Test that a home is stored."""
        cache_path = Path(".test_cache")
        store_to_cache(homes=[home], emails=["no-email"], cache_path=cache_path)
        with cache_path.open() as file:
            assert file.read() == '{"id": "some.url", "email": "no-email"}\n'
        cache_path.unlink()

    def test_multiple_homes_are_stored(self, home: Home, another_home: Home) -> None:
        """Test that multiple homes are stored."""
        cache_path = Path(".test_cache")
        store_to_cache(
            homes=[home, another_home], emails=["no-email"], cache_path=cache_path
        )
        with cache_path.open() as file:
            assert (
                file.read()
                == '{"id": "some.url", "email": "no-email"}\n'
                + '{"id": "another.url", "email": "no-email"}\n'
            )
        cache_path.unlink()

    def test_no_duplicates_are_stored(self, home: Home) -> None:
        """Test that no duplicates are stored."""
        cache_path = Path(".test_cache")
        store_to_cache(homes=[home, home], emails=["no-email"], cache_path=cache_path)
        with cache_path.open() as file:
            assert file.read() == '{"id": "some.url", "email": "no-email"}\n'
        store_to_cache(homes=[home], emails=["no-email"], cache_path=cache_path)
        with cache_path.open() as file:
            assert file.read() == '{"id": "some.url", "email": "no-email"}\n'
        cache_path.unlink()
