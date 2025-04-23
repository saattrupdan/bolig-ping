"""Scraping homes available satisfying the given criteria."""

import logging
import re

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tqdm.auto import tqdm

from .data_models import Home, SearchQuery
from .webdriver import Webdriver

logger = logging.getLogger(__package__)


def scrape_results(search_query: SearchQuery, headless: bool) -> list[Home] | None:
    """Scrape the results of a home search query.

    Args:
        search_query:
            The search query to scrape results for.
        headless:
            Whether to run the WebDriver in headless mode.

    Returns:
        A list of homes that satisfy the search query, or None if no results were found.

    Raises:
        HTTPError:
            If there was an error in the HTTP request.
    """
    url = search_query.get_url()
    logger.info(f"Fetching URL {url!r}...")
    webdriver = Webdriver(headless=headless).load(url=url)

    if "Siden findes ikke" in webdriver.text:
        return None

    # Close the cookie banner
    logger.info("Closing cookie banner...")
    webdriver.click_element_or_ignore(
        xpath="//button[@id='didomi-notice-disagree-button']"
    )

    # Get the number of pages
    logger.info("Getting number of results...")
    try:
        num_results_elt = webdriver.find_element(
            "//h1[contains(concat(' ', normalize-space(@class), ' '), ' text-xl ')]"
        )
    except NoSuchElementException:
        raise ValueError(
            f"Could not find number of results for search query: {search_query}"
        )
    except TimeoutException:
        raise TimeoutError(
            "Timed out while trying to fetch number of results for search query: "
            f"{search_query}."
        )

    num_results_match = re.search(r"[0-9\.]+", num_results_elt.text)
    if num_results_match is None:
        raise ValueError("Could not find number of results.")
    num_results = int(num_results_match.group().replace(".", ""))

    # Extract the homes from the first page
    logger.info("Scraping first page...")
    results = webdriver.find_elements(
        "//div[@data-testid='case-list-card' and "
        "contains(concat(' ', normalize-space(@class), ' '), ' shadow-card ')]"
    )
    homes = [get_home_from_result(result=result) for result in results]

    # Scrape the remaining pages
    with tqdm(desc="Scraping homes from boligsiden.dk", total=num_results) as pbar:
        # Update the progress bar
        pbar.update(len(homes))

        # Calculate the number of pages
        num_pages = num_results // 50
        if num_results % 50 != 0:
            num_pages += 1

        # Iterate over the remaining pages
        for _ in range(num_pages - 1):
            # Go to next page page
            webdriver.click_element_or_ignore(
                xpath="//ul[@role='navigation']//a[@role='button' and @rel='next']"
            )

            # Get the results, where we keep trying in case the page hasn't changed
            # correctly
            num_homes = len(homes)
            new_homes = []
            num_attempts = 3
            while len(homes) == num_homes:
                # Get the results
                results = webdriver.find_elements(
                    "//div["
                    "@data-testid='case-list-card' and contains("
                    "concat(' ', normalize-space(@class), ' '), ' shadow-card ')"
                    "]"
                )
                new_homes = [get_home_from_result(result=result) for result in results]
                homes.extend(new_homes)
                homes = list(set(homes))

                # Monitor the number of attempts and raise an error if we can't change
                # the page
                num_attempts -= 1
                if num_attempts == 0:
                    raise ValueError("Could not change page.")
            pbar.update(len(new_homes))

        # Ensure that the progress bar is at 100% at the end
        pbar.n = pbar.total

    return homes


def get_home_from_result(result: WebElement) -> Home:
    """Get a home from a result.

    Args:
        result:
            The result to get the home from.

    Returns:
        The home from the result.

    Raises:
        ValueError:
            If the result could not be parsed.
    """
    # Extract URL
    candidate_urls = [
        url.get_attribute("href") or ""
        for url in result.find_elements(By.XPATH, ".//a")
        if "viderestilling" in (url.get_attribute("href") or "")
    ]
    if len(candidate_urls) == 0:
        raise ValueError("Could not find URL in result.")
    url = candidate_urls[0].split("?")[0]
    if not url.startswith("https"):
        url = "https://boligsiden.dk" + url

    # Extract address
    try:
        address = result.find_element(
            By.XPATH,
            ".//div["
            "contains(concat(' ', normalize-space(@class), ' '), ' bg-black ')"
            "]//div["
            "contains(concat(' ', normalize-space(@class), ' '), ' font-black ')"
            "]",
        ).text.replace("\n", " ")
    except NoSuchElementException:
        raise ValueError(f"Could not find address in result: {result.text}")

    # Extract span values
    all_span_values = {span.text for span in result.find_elements(By.XPATH, ".//span")}
    span_regexes = dict(
        price=r"kr\.$",
        size=r"[0-9]+ m²",
        num_rooms=r"[0-9]+ Vær",
        monthly_fee=r"Ejerudg.*kr\.?/md",
        year=r"Opført.*[0-9]{4}",
    )
    values = dict()
    for span_value in all_span_values:
        for name, regex in span_regexes.items():
            if re.search(pattern=regex, string=span_value) is not None:
                values[name] = extract_number(span_value)

    return Home(url=url, address=address, **values)


def extract_number(text: str) -> int | None:
    """Extract the number from a string.

    Args:
        text:
            The string containing the number.

    Returns:
        The number, or None if no number was found.
    """
    match = re.search(r"[0-9][0-9\.]*", text)
    if match is None:
        return None
    match_str = match.group().replace(".", "")
    if match_str == "":
        return None
    return int(match_str)
