"""Cache to store already sent homes."""

import json
from pathlib import Path

from .data_models import Home


def store_to_cache(
    homes: list[Home], emails: list[str], cache_path: Path = Path(".bolig_ping_cache")
) -> None:
    """Store the homes to the cache.

    Args:
        homes:
            The homes to store in the cache.
        emails:
            The receiver(s) of the homes.
        cache_path (optional):
            The path to the cache file. Defaults to ".bolig_ping_cache".
    """
    homes = remove_cached_homes(homes=homes, emails=emails, cache_path=cache_path)
    for email in emails:
        added_homes: set[tuple[str, str]] = set()
        with cache_path.open("a") as file:
            for home in homes:
                home_id = home.url.split("/")[-1]
                if (home_id, email) in added_homes:
                    continue
                home_json = json.dumps(dict(id=home_id, email=email))
                file.write(f"{home_json}\n")
                added_homes.add((home_id, email))


def remove_cached_homes(
    homes: list[Home], emails: list[str], cache_path: Path = Path(".bolig_ping_cache")
) -> list[Home]:
    """Remove the cached homes from the list of homes.

    Args:
        homes:
            The homes to remove the cached homes from.
        emails:
            The receiver(s) of the homes.
        cache_path (optional):
            The path to the cache file. Defaults to ".bolig_ping_cache".

    Returns:
        The homes without the cached homes.
    """
    cache_path.touch(exist_ok=True)
    with cache_path.open() as file:
        for line in file:
            json_data = json.loads(line)
            if any(json_data["email"] == email for email in emails):
                homes = [
                    home for home in homes if home.url.split("/")[-1] != json_data["id"]
                ]
    return homes
