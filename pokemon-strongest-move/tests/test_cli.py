from unittest.mock import patch

from pokemon_moves.api import PokeAPIError
from pokemon_moves.cli import clean_name, main


def test_clean_name_lowercases_and_strips():
    assert clean_name("  PIKACHU ") == "pikachu"


def test_clean_name_replaces_spaces_with_hyphens():
    assert clean_name("Mr Mime") == "mr-mime"


@patch("pokemon_moves.cli.find_strongest_move", return_value=("blast-burn", 150))
@patch("pokemon_moves.cli.get_pokemon_moves", return_value=[{"name": "x", "url": "y"}])
@patch("builtins.input", return_value="Charizard")
def test_main_prints_strongest_move(mock_input, mock_moves, mock_find, capsys):
    main()
    assert "Strongest move: blast-burn (Power: 150)" in capsys.readouterr().out


@patch("pokemon_moves.cli.get_pokemon_moves", return_value=None)
@patch("builtins.input", return_value="notapokemon")
def test_main_handles_unknown_pokemon(mock_input, mock_moves, capsys):
    main()
    assert "Couldn't find" in capsys.readouterr().out


@patch("pokemon_moves.cli.get_pokemon_moves", side_effect=PokeAPIError("offline"))
@patch("builtins.input", return_value="pikachu")
def test_main_handles_api_error(mock_input, mock_moves, capsys):
    main()
    assert "Something went wrong" in capsys.readouterr().out


@patch("builtins.input", return_value="   ")
def test_main_handles_empty_input(mock_input, capsys):
    main()
    assert "Please enter" in capsys.readouterr().out
