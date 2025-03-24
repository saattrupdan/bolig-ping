"""Command line interface for the project."""

import logging

import click

from bolig_ping.data_models import SearchQuery
from bolig_ping.scraper import scrape_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s ⋅ %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("jinn")


@click.command("bolig_ping")
@click.option(
    "--area",
    "-a",
    type=str,
    multiple=True,
    required=True,
    help="The area to search for apartments in.",
)
@click.option(
    "--max-price",
    type=int,
    default=int(1e9),
    help="The maximum price of the apartment, in DKK.",
)
@click.option(
    "--min-rooms",
    type=int,
    default=1,
    help="The minimum number of rooms in the apartment.",
)
@click.option(
    "--min-size",
    type=int,
    default=0,
    help="The minimum size of the apartment, in square meters.",
)
@click.option("--query", "-q", multiple=True, help="A query to filter the results by.")
@click.option(
    "--email", type=str, default="", help="Email address to send the notification to."
)
def main(
    area: list[str],
    max_price: int,
    min_rooms: int,
    min_size: int,
    query: list[str],
    email: str | None,
) -> None:
    """Search for flats in a given area of Denmark.

    Args:
        area:
            The area to search for apartments in.
        max_price:
            The maximum price of the apartment, in DKK, or None for no limit.
        min_rooms:
            The minimum number of rooms in the apartment.
        min_size:
            The minimum size of the apartment, in square meters.
        query:
            A query to filter the results by.
        email:
            Email address to send the notification to, or None to print to stdout.
    """
    search_query = SearchQuery(
        areas=area,
        max_price=max_price,
        min_rooms=min_rooms,
        min_size=min_size,
        queries=query,
    )
    results = scrape_results(search_query=search_query)
    logger.info(f"Found {len(results)} flats that satisfy the search query.")


if __name__ == "__main__":
    main()
