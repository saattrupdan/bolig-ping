"""Command line interface for the project."""

import logging
import os
from pathlib import Path

import click
from dotenv import load_dotenv

from .cache import remove_cached_homes, store_to_cache
from .data_models import SearchQuery
from .email import compose_email, send_emails
from .filtering import filter_results
from .scraper import scrape_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s ⋅ %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__package__)

load_dotenv(dotenv_path=".env")


@click.command("bolig_ping")
@click.option(
    "--city", "-c", type=str, multiple=True, help="The city to search for homes in."
)
@click.option(
    "--min-price", type=int, default=None, help="The minimum price of the home, in DKK."
)
@click.option(
    "--max-price", type=int, default=None, help="The maximum price of the home, in DKK."
)
@click.option(
    "--min-monthly-fee",
    type=int,
    default=None,
    help="The minimum monthly fee of the home, in DKK.",
)
@click.option(
    "--max-monthly-fee",
    type=int,
    default=None,
    help="The maximum monthly fee of the home, in DKK.",
)
@click.option(
    "--min-rooms",
    type=int,
    default=None,
    help="The minimum number of rooms in the home.",
)
@click.option(
    "--max-rooms",
    type=int,
    default=None,
    help="The maximum number of rooms in the home.",
)
@click.option(
    "--min-size",
    type=int,
    default=None,
    help="The minimum size of the home, in square meters.",
)
@click.option(
    "--max-size",
    type=int,
    default=None,
    help="The maximum size of the home, in square meters.",
)
@click.option(
    "--query",
    "-q",
    type=str,
    multiple=True,
    help="A keyword that the property description must contain.",
)
@click.option(
    "--property-type",
    "-t",
    type=click.Choice(
        ["ejerlejlighed", "andelslejlighed", "house"], case_sensitive=False
    ),
    multiple=True,
    default=None,
    help="The type of property to search for.",
)
@click.option(
    "--email",
    "-e",
    type=str,
    multiple=True,
    help="Email address to send the notification to. Leave empty to print directly to "
    "the console.",
)
@click.option(
    "--cache/--no-cache",
    default=True,
    show_default=True,
    help="Whether to cache the homes that are found.",
)
def main(
    city: list[str],
    min_price: int | None,
    max_price: int | None,
    min_monthly_fee: int | None,
    max_monthly_fee: int | None,
    min_rooms: int | None,
    max_rooms: int | None,
    min_size: int | None,
    max_size: int | None,
    query: list[str],
    property_type: list[str] | None,
    email: list[str],
    cache: bool,
) -> None:
    """Search for homes in Denmark."""
    # Check if the required environment variables are set
    if email and "GMAIL_EMAIL" not in os.environ:
        logger.error(
            "GMAIL_EMAIL environment variable is not set. Please set it to your "
            "Gmail email address."
        )
        return
    if email and "GMAIL_PASSWORD" not in os.environ:
        logger.error(
            "GMAIL_PASSWORD environment variable is not set. Please set it to your "
            "Gmail app password."
        )
        return

    # Backwards compatibility of cache name
    old_cache_path = Path(".boligping_cache")
    new_cache_path = Path(".bolig_ping_cache")
    if old_cache_path.exists() and not new_cache_path.exists():
        old_cache_path.rename(new_cache_path)
        logger.warning(
            "Renamed the cache file from `.boligping_cache` to `.bolig_ping_cache`."
        )

    search_query = SearchQuery(
        cities=[c.replace("-", " ").lower() for c in city],
        min_price=min_price,
        max_price=max_price,
        min_monthly_fee=min_monthly_fee,
        max_monthly_fee=max_monthly_fee,
        min_rooms=min_rooms,
        max_rooms=max_rooms,
        min_size=min_size,
        max_size=max_size,
        queries=query,
        property_type=property_type,
    )

    if search_query.is_empty():
        logger.warning(
            "No search filters provided. This will return all homes in Denmark! If "
            "this is not what you want, please provide an additional argument. See all "
            "the arguments with `bolig-ping --help`."
        )

    homes = scrape_results(search_query=search_query)
    if homes is None:
        logger.warning("No results found. Double check your search query.")
        return

    if cache:
        homes = remove_cached_homes(homes=homes, emails=email or ["no-email"])
        store_to_cache(homes=homes, emails=email or ["no-email"])

    homes = filter_results(homes=homes, search_query=search_query)
    logger.info(f"Found {len(homes)} new homes that satisfy the search query.")

    if homes:
        if email:
            subject, contents = compose_email(homes=homes)
            send_emails(
                from_email=os.environ["GMAIL_EMAIL"],
                password=os.environ["GMAIL_PASSWORD"],
                to_emails=email,
                subject=subject,
                contents=contents,
            )
            logger.info(f"Sent the homes to {email}.")
        else:
            logger.info(
                "No email provided, so printing the homes here:\n\n"
                + "\n\n".join(home.to_text() for home in homes)
            )


if __name__ == "__main__":
    main()
