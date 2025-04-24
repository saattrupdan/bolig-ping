"""Scraping homes available satisfying the given criteria."""

import json
import logging

import requests
from tqdm.auto import tqdm

from .data_models import Home, SearchQuery

logger = logging.getLogger(__package__)


def scrape_results(search_query: SearchQuery) -> list[Home] | None:
    """Scrape the results of a home search query.

    Args:
        search_query:
            The search query to scrape results for.

    Returns:
        A list of homes that satisfy the search query, or None if no results were found.

    Raises:
        HTTPError:
            If there was an error in the HTTP request.
    """
    logger.info("Fetching results...")

    # Get the results from the search query
    url = search_query.get_url()
    response = requests.get(url=url)
    response.raise_for_status()

    # Parse the response
    result_dict = json.loads(response.text)
    results = result_dict["cases"]
    if results is None:
        return None

    # Get the number of pages
    num_results = result_dict["totalHits"]
    num_pages = num_results // len(results)
    if num_results % len(results) != 0:
        num_pages += 1

    # Get the first page of results
    homes = [get_home_from_result(result=result) for result in results]

    # Scrape the remaining pages
    if num_pages > 1:
        with tqdm(desc="Scraping homes from boligsiden.dk", total=num_results) as pbar:
            pbar.update(len(homes))
            for page_idx in range(2, num_pages + 1):
                url = search_query.get_url(page=page_idx)
                response = requests.get(url=url)
                response.raise_for_status()
                result_dict = json.loads(response.text)
                results = result_dict["cases"]
                new_homes = [get_home_from_result(result=result) for result in results]
                homes.extend(new_homes)
                homes = list(set(homes))
                pbar.update(len(new_homes))

        # Ensure that the progress bar is at 100% at the end
        pbar.n = pbar.total

    return homes


def get_home_from_result(result: dict) -> Home:
    """Get a home from a result.

    Args:
        result:
            The result to get the home from.

    Returns:
        The home from the result.
    """
    url = f"https://boligsiden.dk/viderestilling/{result['caseID']}"
    road_name = result["address"]["roadName"]
    road_number = result["address"].get("houseNumber")
    floor = result["address"].get("floor")
    door = result["address"].get("door")
    post_code = result["address"].get("zipCode")
    city = result["address"]["cityName"]

    address = road_name
    if road_number:
        address += f" {road_number}"
    if floor:
        floor = floor.replace("0", "st.")
        address += f" {floor}"
    if door:
        address += f" {door}"
    if post_code:
        address += f" {post_code}"
    if city:
        address += f" {city}"

    return Home(
        url=url,
        address=address,
        price=result.get("priceCash"),
        num_rooms=result.get("numberOfRooms"),
        size=result.get("housingArea"),
        monthly_fee=result.get("monthlyExpense"),
        year=result.get("yearBuilt"),
    )
