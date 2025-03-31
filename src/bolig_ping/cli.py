"""Command line interface for the project."""

import logging
import os

import click

from .cache import remove_cached_flats, store_to_cache
from .data_models import SearchQuery
from .email import compose_email, send_email
from .scraper import scrape_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s ⋅ %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__package__)


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
    "--min-price",
    type=int,
    default=0,
    show_default=True,
    help="The minimum price of the apartment, in DKK.",
)
@click.option(
    "--max-price",
    type=int,
    default=int(1e9),
    show_default=True,
    help="The maximum price of the apartment, in DKK.",
)
@click.option(
    "--min-rooms",
    type=int,
    default=1,
    show_default=True,
    help="The minimum number of rooms in the apartment.",
)
@click.option(
    "--max-rooms",
    type=int,
    default=int(1e9),
    show_default=True,
    help="The maximum number of rooms in the apartment.",
)
@click.option(
    "--min-size",
    type=int,
    default=0,
    show_default=True,
    help="The minimum size of the apartment, in square meters.",
)
@click.option(
    "--max-size",
    type=int,
    default=int(1e9),
    show_default=True,
    help="The maximum size of the apartment, in square meters.",
)
@click.option(
    "--email",
    type=str,
    default=None,
    show_default=True,
    help="Email address to send the notification to, or None to print to stdout.",
)
@click.option("--query", "-q", multiple=True, help="A query to filter the results by.")
def main(
    city: list[str],
    min_price: int,
    max_price: int,
    min_rooms: int,
    max_rooms: int,
    min_size: int,
    max_size: int,
    query: list[str],
    email: str | None,
) -> None:
    """Search for flats in Denmark."""
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
        min_price=min_price,
        max_price=max_price,
        min_rooms=min_rooms,
        max_rooms=max_rooms,
        min_size=min_size,
        max_size=max_size,
        queries=query,
    )
    flats = scrape_results(search_query=search_query)
    flats = remove_cached_flats(flats=flats, email=email or "no-email")
    logger.info(f"Found {len(flats)} new flats that satisfy the search query.")
    if flats:
        if email is not None:
            subject, contents = compose_email(flats=flats)
            send_email(
                from_email=os.environ["GMAIL_EMAIL"],
                password=os.environ["GMAIL_PASSWORD"],
                to_email=email,
                subject=subject,
                contents=contents,
            )
            logger.info(f"Sent the flats to {email}.")
        else:
            logger.info(
                "No email provided, so printing the flats here:\n\n"
                + "\n\n".join(flat.to_html() for flat in flats)
            )
        store_to_cache(flats=flats, email=email or "no-email")


if __name__ == "__main__":
    main()
