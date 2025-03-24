"""Data models used in the project."""

from pydantic import BaseModel


class SearchQuery(BaseModel):
    """A flat search query."""

    areas: list[str]
    max_price: int
    min_rooms: int
    min_size: int
    queries: list[str]

    def get_url(self) -> str:
        """Get the URL for the search query.

        Returns:
            The URL for the search query.
        """
        url = "https://www.boligsiden.dk/by/{}/tilsalg/ejerlejlighed".format(
            ",".join(self.areas)
        )
        arguments: dict[str, str | int] = dict(
            priceMax=self.max_price,
            numberOfRoomsMin=self.min_rooms,
            areaMin=self.min_size,
        )
        if self.queries:
            arguments["text"] = ",".join(self.queries)
        url += "?" + "&".join(f"{key}={value}" for key, value in arguments.items())
        return url


class Flat(BaseModel):
    """A flat listing."""

    url: str
    price: int | None
    size: int | None
    monthly_fee: int | None
    year: int | None

    def __hash__(self) -> int:
        """Get the hash of the flat.

        Returns:
            The hash of the flat.
        """
        return hash(self.url)
