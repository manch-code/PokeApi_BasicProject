from unittest.mock import Mock, patch

import requests

from pokemon_moves.api import PokeAPIError, get_move_power, get_pokemon_moves


@patch("pokemon_moves.api.requests.get")
def test_unknown_pokemon_returns_none(mock_get):
    mock_get.return_value = Mock(status_code=404)
    assert get_pokemon_moves("notapokemon") is None


@patch("pokemon_moves.api.requests.get")
def test_get_pokemon_moves_returns_move_list(mock_get):
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {"moves": [{"move": {"name": "ember", "url": "url/ember"}}]},
    )
    assert get_pokemon_moves("charmander") == [{"name": "ember", "url": "url/ember"}]


@patch("pokemon_moves.api.requests.get")
def test_network_error_raises_pokeapi_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("offline")
    try:
        get_pokemon_moves("pikachu")
    except PokeAPIError:
        return
    raise AssertionError("PokeAPIError was not raised")


@patch("pokemon_moves.api.requests.get")
def test_server_error_raises_pokeapi_error(mock_get):
    mock_get.return_value = Mock(status_code=500)
    try:
        get_pokemon_moves("pikachu")
    except PokeAPIError:
        return
    raise AssertionError("PokeAPIError was not raised")


@patch("pokemon_moves.api.requests.get")
def test_status_move_has_no_power(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"power": None})
    assert get_move_power("url/growl") is None


@patch("pokemon_moves.api.requests.get")
def test_damaging_move_returns_power(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"power": 150})
    assert get_move_power("url/blast-burn") == 150


@patch("pokemon_moves.api.requests.get")
def test_failed_move_request_returns_none(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()
    assert get_move_power("url/ember") is None
