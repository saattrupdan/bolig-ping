"""Data models used in the project."""

import logging
from functools import cached_property
from typing import Any

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

logger = logging.getLogger(__package__)


class SearchQuery(BaseModel):
    """A search query."""

    cities: list[str] = Field(default_factory=list)
    min_price: int | None = Field(default=None, ge=0)
    max_price: int | None = Field(default=None, ge=0)
    min_monthly_fee: int | None = Field(default=None, ge=0)
    max_monthly_fee: int | None = Field(default=None, ge=0)
    min_rooms: int | None = Field(default=None, ge=1)
    max_rooms: int | None = Field(default=None, ge=1)
    min_size: int | None = Field(default=None, ge=1)
    max_size: int | None = Field(default=None, ge=1)
    queries: list[str] = Field(default_factory=list)
    property_type: list[str] | None = Field(default=None)

    def is_empty(self) -> bool:
        """Check if the search query is empty.

        Returns:
            True if the search query is empty, False otherwise.
        """
        return (
            not self.cities
            and self.min_price is None
            and self.max_price is None
            and self.min_rooms is None
            and self.max_rooms is None
            and self.min_size is None
            and self.max_size is None
        )

    def get_url(self, page: int = 1) -> str:
        """Get the URL for the search query.

        Args:
            page (optional):
                The page number to get the URL for. Defaults to 1.

        Returns:
            The URL for the search query.
        """
        url = f"https://api.boligsiden.dk/search/cases?page={page}"

        property_type_names: list[str] = []
        if self.property_type is not None:
            if "ejerlejlighed" in self.property_type:
                property_type_names.extend(["condo", "villa apartment"])
            if "andelslejlighed" in self.property_type:
                property_type_names.append("cooperative")
            if "house" in self.property_type:
                property_type_names.extend(["terraced house", "villa", "farm"])
            property_type_names = sorted(set(property_type_names))

        arguments: dict[str, Any] = dict(
            addressTypes=",".join(property_type_names) if property_type_names else None,
            cities=self.cities or None,
            priceMin=self.min_price,
            priceMax=self.max_price,
            numberOfRoomsMin=self.min_rooms,
            numberOfRoomsMax=self.max_rooms,
            areaMin=self.min_size,
            areaMax=self.max_size,
            monthlyExpenseMin=self.min_monthly_fee,
            monthlyExpenseMax=self.max_monthly_fee,
        )
        non_trivial_arguments = {
            key: value for key, value in arguments.items() if value is not None
        }
        if non_trivial_arguments:
            for key, value in non_trivial_arguments.items():
                if not isinstance(value, list):
                    value = [value]
                for item in value:
                    url += f"&{key}={item}"

        return url


class Home(BaseModel):
    """A property listing."""

    url: str
    address: str
    price: int | None = Field(default=None, ge=0)
    num_rooms: int | None = Field(default=None, ge=1)
    size: int | None = Field(default=None, ge=1)
    monthly_fee: int | None = Field(default=None, ge=0)
    year: int | None = Field(default=None, ge=0)

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
        components = [f"<a href='{self.url}'>{self.address}</a>"]
        if self.price is not None:
            components.append(f"Price: {self.price:,} kr.")
        if self.num_rooms is not None:
            components.append(f"Number of rooms: {self.num_rooms}")
        if self.size is not None:
            components.append(f"Size: {self.size} m²")
        if self.monthly_fee is not None:
            components.append(f"Monthly fee: {self.monthly_fee:,} kr./md")
        if self.year is not None:
            components.append(f"Year built: {self.year}")
        return "\n".join(components)

    def to_text(self) -> str:
        """Get the home as a text string.

        Returns:
            The home as a text string.
        """
        components = [f"URL: {self.url}", f"Address: {self.address}"]
        if self.price is not None:
            components.append(f"Price: {self.price:,} kr.")
        if self.num_rooms is not None:
            components.append(f"Number of rooms: {self.num_rooms}")
        if self.size is not None:
            components.append(f"Size: {self.size} m²")
        if self.monthly_fee is not None:
            components.append(f"Monthly fee: {self.monthly_fee:,} kr./md")
        if self.year is not None:
            components.append(f"Year built: {self.year}")
        return "\n".join(components)
