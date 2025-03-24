"""Exceptions used throughout the project."""


class ScraperError(Exception):
    """An error occurred while scraping."""

    def __init__(self, url: str, message: str | None = None) -> None:
        """Initialise the error.

        Args:
            url:
                The URL of the page that caused the error.
            message:
                The error message.
        """
        if message is None:
            message = f"An error occurred while fetching {url!r}."
        self.url = url
        self.message = message
        super().__init__(message)


class Timeout(ScraperError):
    """A timeout occurred while scraping."""

    def __init__(self, url: str) -> None:
        """Initialise the error.

        Args:
            url:
                The URL of the page that caused the error.
        """
        super().__init__(url=url, message=f"Timeout while fetching {url!r}.")


class ElementDoesNotExist(ScraperError):
    """A HTML element does not exist."""

    def __init__(self, url: str, xpath: str) -> None:
        """Initialise the error.

        Args:
            url:
                The URL of the page that caused the error.
            xpath:
                The XPath of the element that does not exist.
        """
        super().__init__(
            url=url, message=f"Element {xpath!r} does not exist on {url!r}."
        )


class MaximumRetriesReached(ScraperError):
    """The maximum number of retries was reached."""

    def __init__(self, url: str) -> None:
        """Initialise the error.

        Args:
            url:
                The URL of the page that caused the error.
        """
        super().__init__(
            url=url, message=f"Maximum number of retries reached for {url!r}."
        )


class ChromeHasCrashed(ScraperError):
    """Chrome has crashed."""

    def __init__(self) -> None:
        """Initialise the error."""
        super().__init__(url="", message="Chrome has crashed.")
