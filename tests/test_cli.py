"""Tests for the `cli` module."""

from collections.abc import Generator

import pytest
from click.testing import CliRunner

from bolig_ping.cli import main


@pytest.fixture(scope="module")
def runner() -> Generator[CliRunner, None, None]:
    """Fixture for the CLI runner."""
    yield CliRunner()


@pytest.mark.parametrize(
    argnames=["cli_args"],
    argvalues=[
        ("--city københavn-n",),
        ("--city københavn-n --city brøndby",),
        ("--city københavn-n --max-price 100",),
        ("--city københavn-n --city brøndby --max-price 100",),
        ("--max-price 100",),
    ],
    ids=[
        "city",
        "multiple-cities",
        "city-and-max-price",
        "multiple-cities-and-max-price",
        "no-city",
    ],
)
def test_main(cli_args: str, runner: CliRunner) -> None:
    """Test the main function."""
    result = runner.invoke(cli=main, args=cli_args)
    assert result.exit_code == 0
