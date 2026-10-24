"""Command-line interface."""

from pokemon_moves.api import PokeAPIError, get_pokemon_moves
from pokemon_moves.finder import find_strongest_move


def clean_name(raw_name):
    """
    Turn user input into the format PokeAPI expects.

    >>> clean_name("  Mr Mime ")
    'mr-mime'
    """
    return "-".join(raw_name.strip().lower().split())


def main():
    name = clean_name(input("Enter a Pokémon name: "))

    if not name:
        print("Please enter a Pokémon name.")
        return

    print("Searching... this may take a few seconds.")

    try:
        moves = get_pokemon_moves(name)
    except PokeAPIError as error:
        print(f"Something went wrong: {error}")
        return

    if moves is None:
        print(f"Couldn't find a Pokémon named '{name}'. Check the spelling and try again.")
        return

    result = find_strongest_move(moves, show_progress=True)

    if result is None:
        print(f"{name} has no damaging moves.")
        return

    move_name, power = result
    print(f"Strongest move: {move_name} (Power: {power})")
