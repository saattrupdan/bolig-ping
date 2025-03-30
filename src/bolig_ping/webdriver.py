"""Webdriver used for scraping."""

import logging
from time import sleep

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.common.exceptions import (
    NoSuchElementException,
    SessionNotCreatedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__package__)


class Webdriver:
    """A WebDriver to use for scraping."""

    def __init__(
        self,
        num_attempts: int = 3,
        timeout: int = 10,
        sleep_time: int = 3,
        headless: bool = True,
        **_,
    ) -> None:
        """Initialise the WebDriver.

        Args:
            num_attempts:
                The maximum number of attempts to get a page.
            timeout:
                The maximum time to wait for a page to load, in seconds.
            sleep_time:
                The time to sleep between attempts, in seconds.
            headless:
                Whether to run the WebDriver in headless mode.
        """
        self.num_attempts = num_attempts
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.headless = headless
        self.driver = self.get_driver()

    @property
    def html(self) -> str:
        """Get the HTML of the current page.

        Returns:
            The HTML of the current page.
        """
        return self.driver.page_source

    def get_driver(self) -> webdriver.Chrome:
        """Get the WebDriver options.

        Returns:
            The WebDriver options.
        """
        options = webdriver.ChromeOptions()

        chrome_arguments = [
            "--no-sandbox",
            "--remote-debugging-port=9222",
            "--remote-debugging-pipe",
            "--autoplay-policy=no-user-gesture-required",
            "--no-first-run",
            "--disable-gpu",
            "--use-fake-ui-for-media-stream",
            "--use-fake-device-for-media-stream",
            "--disable-sync",
            "--disable-dev-shm-usage",
            "--start-maximized",
        ]
        for argument in chrome_arguments:
            options.add_argument(argument=argument)

        if self.headless:
            options.add_argument("--headless=new")

        attempts = 3
        for _ in range(attempts):
            try:
                driver = webdriver.Chrome(options=options)
                break
            except SessionNotCreatedException:
                logger.error("Could not create a new session. Trying again...")
                sleep(3)
        else:
            raise ConnectionError("Could not create a new session.")

        driver.set_page_load_timeout(time_to_wait=self.timeout)
        return driver

    def load(self, url: str) -> "Webdriver":
        """Load the DOM of a web page.

        Args:
            url:
                The URL of the web page.

        Raises:
            ConnectionError:
                If the page couldn't load.
        """
        for _ in range(self.num_attempts):
            try:
                self.driver.get(url=url)
                sleep(self.sleep_time)
                return self
            except (WebDriverException, TimeoutException) as e:
                logger.error(
                    f"{type(e).__name__} occurred while fetching the web page {url!r}. "
                    f"Retrying..."
                )
                sleep(self.sleep_time)
                return self
        else:
            raise ConnectionError(f"Could not load website {url}.")

    def find_element(self, xpath: str) -> WebElement:
        """Find an element by XPath.

        Args:
            xpath:
                The XPath of the element.

        Returns:
            The element found by the XPath, or None if not found.
        """
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def find_elements(self, xpath: str) -> list[WebElement]:
        """Find elements by XPath.

        Args:
            xpath:
                The XPath of the elements.

        Returns:
            The elements found by the XPath.
        """
        return self.driver.find_elements(by=By.XPATH, value=xpath)

    def click_element_or_ignore(self, xpath: str) -> None:
        """Click an element by XPath, or ignore if not found.

        Args:
            xpath:
                The XPath of the element.
        """
        try:
            self.find_element(xpath=xpath).click()
            sleep(3)
        except NoSuchElementException:
            pass
