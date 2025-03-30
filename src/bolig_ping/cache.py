"""Cache to store already sent flats."""

import json
from pathlib import Path

from .data_models import Flat


def store_to_cache(
    flats: list[Flat], email: str, cache_path: Path = Path(".boligping_cache")
) -> None:
    """Store the flats to the cache.

    Args:
        flats:
            The flats to store in the cache.
        email:
            The receiver of the flats.
        cache_path (optional):
            The path to the cache file. Defaults to ".boligping_cache".
    """
    flats = remove_cached_flats(flats=flats, email=email, cache_path=cache_path)
    added_flats: set[tuple[str, str]] = set()
    with cache_path.open("a") as file:
        for flat in flats:
            flat_id = flat.url.split("/")[-1]
            if (flat_id, email) in added_flats:
                continue
            flat_json = json.dumps(dict(id=flat_id, email=email))
            file.write(f"{flat_json}\n")
            added_flats.add((flat_id, email))


def remove_cached_flats(
    flats: list[Flat], email: str, cache_path: Path = Path(".boligping_cache")
) -> list[Flat]:
    """Remove the cached flats from the list of flats.

    Args:
        flats:
            The flats to remove the cached flats from.
        email:
            The receiver of the flats.
        cache_path (optional):
            The path to the cache file. Defaults to ".boligping_cache".

    Returns:
        The flats without the cached flats.
    """
    cache_path.touch(exist_ok=True)
    with cache_path.open() as file:
        for line in file:
            json_data = json.loads(line)
            if json_data["email"] == email:
                flats = [
                    flat for flat in flats if flat.url.split("/")[-1] != json_data["id"]
                ]
    return flats
