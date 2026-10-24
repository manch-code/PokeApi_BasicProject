"""Logic for choosing the strongest move."""

from pokemon_moves.api import get_move_power

PROGRESS_EVERY = 20


def find_strongest_move(moves, show_progress=False):
    """
    Given a list of moves (dicts with "name" and "url"),
    return (move_name, power) for the strongest one.
    Return None if no move has any power.

    If several moves tie for the highest power, the first one found wins.
    """
    strongest_name = None
    strongest_power = 0
    total = len(moves)

    for index, move in enumerate(moves, start=1):
        power = get_move_power(move["url"])

        if show_progress and index % PROGRESS_EVERY == 0:
            print(f"  Checked {index}/{total} moves...")

        if power is None:
            continue  # Status moves like Growl have no power

        if power > strongest_power:
            strongest_name = move["name"]
            strongest_power = power

    if strongest_name is None:
        return None

    return strongest_name, strongest_power
