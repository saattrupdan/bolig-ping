"""Tests for the `cli` module."""

import pytest
from click.testing import CliRunner

from bolig_ping.cli import main


@pytest.mark.parametrize(
    argnames=["cli_args"],
    argvalues=[
        ("--city københavn-n --max-price 100",),
        ("--city københavn-n --city brøndby --max-price 100",),
    ],
    ids=["One city", "Multiple cities"],
)
def test_main(cli_args: str) -> None:
    """Test the main function."""
    runner = CliRunner()
    result = runner.invoke(cli=main, args=cli_args)
    assert result.exit_code == 0
