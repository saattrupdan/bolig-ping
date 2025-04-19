"""Command line interface for the project."""

import logging
import os

import click

from .cache import remove_cached_homes, store_to_cache
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
    "--min-monthly-fee",
    type=int,
    default=0,
    show_default=True,
    help="The minimum monthly fee of the apartment, in DKK.",
)
@click.option(
    "--max-monthly-fee",
    type=int,
    default=int(1e9),
    show_default=True,
    help="The maximum monthly fee of the apartment, in DKK.",
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
    "--query",
    "-q",
    multiple=True,
    help="A keyword that the home description must contain.",
)
@click.option(
    "--property-type",
    "-t",
    type=click.Choice(["ejerlejlighed", "andelslejlighed", "house"]),
    multiple=True,
    default=None,
    help="The type of property to search for. Default is only searching for "
    "'ejerlejlighed'.",
)
@click.option(
    "--email",
    type=str,
    default=None,
    show_default=True,
    help="Email address to send the notification to, or None to print to stdout.",
)
@click.option(
    "--cache/--no-cache",
    default=True,
    show_default=True,
    help="Whether to cache the homes that are found.",
)
def main(
    city: list[str],
    min_price: int,
    max_price: int,
    min_monthly_fee: int,
    max_monthly_fee: int,
    min_rooms: int,
    max_rooms: int,
    min_size: int,
    max_size: int,
    query: list[str],
    property_type: list[str],
    email: str | None,
    cache: bool,
) -> None:
    """Search for homes in Denmark."""
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
        min_monthly_fee=min_monthly_fee,
        max_monthly_fee=max_monthly_fee,
        min_rooms=min_rooms,
        max_rooms=max_rooms,
        min_size=min_size,
        max_size=max_size,
        queries=query,
        property_type=property_type or ["ejerlejlighed"],
    )
    homes = scrape_results(search_query=search_query)
    if homes is None:
        logger.error(
            "Could not find the city that you requested. Please double check the "
            "spelling of the city name(s) and try again."
        )
        return
    if cache:
        homes = remove_cached_homes(homes=homes, email=email or "no-email")

    logger.info(f"Found {len(homes)} new homes that satisfy the search query.")

    if homes:
        if email is not None:
            subject, contents = compose_email(homes=homes)
            send_email(
                from_email=os.environ["GMAIL_EMAIL"],
                password=os.environ["GMAIL_PASSWORD"],
                to_email=email,
                subject=subject,
                contents=contents,
            )
            logger.info(f"Sent the homes to {email}.")
        else:
            logger.info(
                "No email provided, so printing the homes here:\n\n"
                + "\n\n".join(home.to_text() for home in homes)
            )
        if cache:
            store_to_cache(homes=homes, email=email or "no-email")


if __name__ == "__main__":
    main()
