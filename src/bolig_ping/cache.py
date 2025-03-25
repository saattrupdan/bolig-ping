"""Cache to store already sent flats."""

import json
from pathlib import Path

from .data_models import Flat


def store_to_cache(flats: list[Flat], email: str) -> None:
    """Store the flats to the cache.

    Args:
        flats:
            The flats to store in the cache.
        email:
            The receiver of the flats.
    """
    flats = remove_cached_flats(flats=flats, email=email)
    cache_path = Path(".boligping_cache")
    with cache_path.open("a") as file:
        for flat in flats:
            flat_id = flat.url.split("/")[-1]
            flat_json = json.dumps(dict(id=flat_id, email=email))
            file.write(f"{flat_json}\n")


def remove_cached_flats(flats: list[Flat], email: str) -> list[Flat]:
    """Remove the cached flats from the list of flats.

    Args:
        flats:
            The flats to remove the cached flats from.
        email:
            The receiver of the flats.

    Returns:
        The flats without the cached flats.
    """
    cache_path = Path(".boligping_cache")
    cache_path.touch(exist_ok=True)
    with cache_path.open() as file:
        for line in file:
            json_data = json.loads(line)
            if json_data["email"] == email:
                flats = [
                    flat for flat in flats if flat.url.split("/")[-1] != json_data["id"]
                ]
    return flats
