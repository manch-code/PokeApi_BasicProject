from unittest.mock import patch

from pokemon_moves.finder import find_strongest_move

MOVES = [
    {"name": "growl", "url": "url/growl"},
    {"name": "ember", "url": "url/ember"},
    {"name": "blast-burn", "url": "url/blast-burn"},
]

POWERS = {"url/growl": None, "url/ember": 40, "url/blast-burn": 150}


@patch("pokemon_moves.finder.get_move_power", side_effect=lambda url: POWERS[url])
def test_returns_highest_power_move(mock_power):
    assert find_strongest_move(MOVES) == ("blast-burn", 150)


@patch("pokemon_moves.finder.get_move_power", return_value=None)
def test_returns_none_when_no_move_has_power(mock_power):
    assert find_strongest_move(MOVES) is None


def test_empty_move_list_returns_none():
    assert find_strongest_move([]) is None


@patch("pokemon_moves.finder.get_move_power", return_value=90)
def test_tie_returns_first_move_found(mock_power):
    assert find_strongest_move(MOVES) == ("growl", 90)
