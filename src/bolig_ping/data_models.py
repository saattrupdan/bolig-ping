"""Data models used in the project."""

import logging
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger(__package__)


class SearchQuery(BaseModel):
    """A search query."""

    cities: list[str]
    min_price: int
    max_price: int
    min_monthly_fee: int
    max_monthly_fee: int
    min_rooms: int
    max_rooms: int
    min_size: int
    max_size: int
    queries: list[str]
    property_type: list[str]

    def get_url(self) -> str:
        """Get the URL for the search query.

        Returns:
            The URL for the search query.
        """
        property_type_names: list[str] = []
        if "ejerlejlighed" in self.property_type:
            property_type_names.extend(["ejerlejlighed", "villalejlighed"])
        if "andelslejlighed" in self.property_type:
            property_type_names.append("andelslejlighed")
        if "house" in self.property_type:
            property_type_names.extend(["raekkehus", "villa", "landejendom"])
        property_type_names = sorted(set(property_type_names))

        url = "https://www.boligsiden.dk/by/{}/tilsalg/{}".format(
            ",".join(self.cities), ",".join(property_type_names)
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


class Home(BaseModel):
    """A property listing."""

    url: str
    address: str
    price: int | None
    num_rooms: int | None
    size: int | None
    monthly_fee: int | None
    year: int | None

    @cached_property
    def description(self) -> str | None:
        """Get the description of the home.

        Returns:
            The description of the home, or None if not available.
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
                    f"Could not find description for property {self.url}. The longest "
                    f"line was {max(len(line) for line in lines)} characters long."
                )
        return None

    def __hash__(self) -> int:
        """Get the hash of the home.

        Returns:
            The hash of the home.
        """
        return hash(self.url)

    def to_html(self) -> str:
        """Get the home as an HTML string.

        Returns:
            The home as an HTML string.
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
        """Get the home as a text string.

        Returns:
            The home as a text string.
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
