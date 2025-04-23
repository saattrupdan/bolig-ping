"""Filtering of scraped results."""

from tqdm.auto import tqdm

from .data_models import Home, SearchQuery


def filter_results(homes: list[Home], search_query: SearchQuery) -> list[Home]:
    """Filter the homes based on the given criteria.

    Args:
        homes:
            The homes to filter.
        search_query:
            The search query to filter the homes by.

    Returns:
        The filtered homes.
    """
    # Filter the homes based on the monthly fee
    homes = [
        home
        for home in homes
        if home.monthly_fee is None
        or (
            (
                search_query.min_monthly_fee is None
                or home.monthly_fee >= search_query.min_monthly_fee
            )
            and (
                search_query.max_monthly_fee is None
                or home.monthly_fee <= search_query.max_monthly_fee
            )
        )
    ]

    # Filter the homes if any keyword queries were given
    if search_query.queries:
        homes = [
            home
            for home in tqdm(iterable=homes, desc="Filtering homes based on keywords")
            if home.description is not None
            and any(
                query.lower() in home.description.lower()
                for query in search_query.queries
            )
        ]

    return homes
