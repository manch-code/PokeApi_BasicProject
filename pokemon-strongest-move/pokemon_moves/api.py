"""Functions that talk to PokeAPI."""

import requests

BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT_SECONDS = 10


class PokeAPIError(Exception):
    """Raised when PokeAPI can't be reached or returns an unexpected error."""


def get_pokemon_moves(name):
    """
    Return a list of moves the Pokémon can learn.
    Each item is a dict with the move's "name" and "url".
    Return None if the Pokémon isn't found.
    Raise PokeAPIError if the API can't be reached or fails.
    """
    url = f"{BASE_URL}/pokemon/{name}"

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.RequestException as error:
        raise PokeAPIError(f"Could not reach PokeAPI: {error}") from error

    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise PokeAPIError(f"PokeAPI returned status {response.status_code}.")

    data = response.json()

    # Each entry looks like: {"move": {"name": "...", "url": "..."}, ...}
    return [
        {"name": entry["move"]["name"], "url": entry["move"]["url"]}
        for entry in data["moves"]
    ]


def get_move_power(move_url):
    """
    Request one move's details and return its power.
    Returns None for status moves (like Growl) that have no power,
    or if this one request fails (so a single bad move doesn't crash the search).
    """
    try:
        response = requests.get(move_url, timeout=TIMEOUT_SECONDS)
        if response.status_code != 200:
            return None
        return response.json().get("power")
    except (requests.exceptions.RequestException, ValueError):
        return None
