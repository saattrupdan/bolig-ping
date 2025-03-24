"""Command line interface for the project."""

import logging
from time import sleep

import click

from .cache import remove_cached_flats, store_to_cache
from .data_models import SearchQuery
from .email import send_flats
from .scraper import scrape_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s ⋅ %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("jinn")


@click.command("bolig_ping")
@click.option(
    "--city",
    "-c",
    type=str,
    multiple=True,
    required=True,
    help="The city to search for apartments in.",
)
@click.option(
    "--email",
    "-e",
    type=str,
    required=True,
    help="Email address to send the notification to.",
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
    "--update-interval-hours",
    type=int,
    default=None,
    help="The interval in hours to update the search results. If None, only run once.",
)
def main(
    city: list[str],
    email: str,
    max_price: int,
    min_rooms: int,
    min_size: int,
    query: list[str],
    update_interval_hours: int | None,
) -> None:
    """Search for flats in Denmark.

    Args:
        city:
            The city to search for apartments in.
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
        update_interval_hours:
            The interval in hours to update the search results. If None, only run once.
    """
    cities = [
        c.replace(" ", "-")
        .replace("ø", "oe")
        .replace("æ", "ae")
        .replace("å", "aa")
        .lower()
        for c in city
    ]
    search_query = SearchQuery(
        cities=cities,
        max_price=max_price,
        min_rooms=min_rooms,
        min_size=min_size,
        queries=query,
    )
    if update_interval_hours is None:
        find_new_flats(search_query=search_query, email=email)
    else:
        while True:
            find_new_flats(search_query=search_query, email=email)
            logger.info(f"Sleeping for {update_interval_hours:,} hours...")
            sleep(update_interval_hours * 3600)


def find_new_flats(search_query: SearchQuery, email: str) -> None:
    """Find new flats that satisfy the search query and send them to the email.

    Args:
        search_query:
            The search query to find flats for.
        email:
            The email to send the flats to.
    """
    flats = scrape_results(search_query=search_query)
    flats = remove_cached_flats(flats=flats, email=email)
    logger.info(f"Found {len(flats)} new flats that satisfy the search query.")
    if flats:
        send_flats(to_email=email, flats=flats)
        store_to_cache(flats=flats, email=email)
        logger.info(f"Sent the flats to {email}.")


if __name__ == "__main__":
    main()
