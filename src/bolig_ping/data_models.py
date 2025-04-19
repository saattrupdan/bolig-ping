"""Data models used in the project."""

import logging
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger(__package__)


class SearchQuery(BaseModel):
    """A flat search query."""

    cities: list[str]
    min_price: int
    max_price: int
    min_rooms: int
    max_rooms: int
    min_size: int
    max_size: int
    queries: list[str]

    def get_url(self) -> str:
        """Get the URL for the search query.

        Returns:
            The URL for the search query.
        """
        url = "https://www.boligsiden.dk/by/{}/tilsalg/ejerlejlighed".format(
            ",".join(self.cities)
        )
        arguments: dict[str, str | int] = dict(
            priceMin=self.min_price,
            priceMax=self.max_price,
            numberOfRoomsMin=self.min_rooms,
            numberOfRoomsMax=self.max_rooms,
            areaMin=self.min_size,
            areaMax=self.max_size,
        )
        url += "?" + "&".join(f"{key}={value}" for key, value in arguments.items())
        return url


class Flat(BaseModel):
    """A flat listing."""

    url: str
    address: str
    price: int | None
    num_rooms: int | None
    size: int | None
    monthly_fee: int | None
    year: int | None

    @cached_property
    def description(self) -> str | None:
        """Get the description of the flat.

        Returns:
            The description of the flat, or None if not available.
        """
        response = requests.get(url=self.url)
        if response.ok:
            soup = BeautifulSoup(response.content, "html.parser")
            lines = soup.text.split("\n")
            long_lines = [line.strip() for line in lines if len(line.strip()) > 200]
            if long_lines:
                return "\n".join(long_lines)
            else:
                logger.warning(
                    f"Could not find description for flat {self.url}. The longest line "
                    f"was {max(len(line) for line in lines)} characters long."
                )
        return None

    def __hash__(self) -> int:
        """Get the hash of the flat.

        Returns:
            The hash of the flat.
        """
        return hash(self.url)

    def to_html(self) -> str:
        """Get the flat as an HTML string.

        Returns:
            The flat as an HTML string.
        """
        html = "\n".join(
            [
                f"<a href='{self.url}'>{self.address}</a>",
                f"Price: {self.price:,} kr.",
                f"Number of rooms: {self.num_rooms}",
                f"Size: {self.size} m²",
                f"Monthly fee: {self.monthly_fee:,} kr./md",
                f"Year built: {self.year}",
            ]
        )
        return html

    def to_text(self) -> str:
        """Get the flat as a text string.

        Returns:
            The flat as a text string.
        """
        text = "\n".join(
            [
                f"URL: {self.url}",
                f"Address: {self.address}",
                f"Price: {self.price:,} kr.",
                f"Number of rooms: {self.num_rooms}",
                f"Size: {self.size} m²",
                f"Monthly fee: {self.monthly_fee:,} kr./md",
                f"Year built: {self.year}",
            ]
        )
        return text
