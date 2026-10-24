# Pokémon Strongest Move Finder

A Python command-line app that uses [PokeAPI](https://pokeapi.co) to find the
highest base-power move a Pokémon can learn.

```
$ python -m pokemon_moves
Enter a Pokémon name: charizard
Searching... this may take a few seconds.
Strongest move: blast-burn (Power: 150)
```

## Features
- Looks up any Pokémon by name (case and whitespace insensitive)
- Checks every learnable move and skips status moves with no power
- Friendly error messages for bad names and network problems
- Progress updates while it checks moves
- Unit tests (with mocked API responses) and a GitHub Actions workflow

## Getting Started

### Prerequisites
- Python 3.9+

### Installation
```bash
git clone https://github.com/<your-username>/pokemon-strongest-move.git
cd pokemon-strongest-move

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Usage
```bash
python -m pokemon_moves
```

## Running Tests
```bash
pip install -r requirements-dev.txt
pytest
```

## Project Structure
```
pokemon-strongest-move/
├── pokemon_moves/
│   ├── __init__.py
│   ├── __main__.py     # Enables `python -m pokemon_moves`
│   ├── api.py          # Talks to PokeAPI (HTTP requests)
│   ├── finder.py       # Logic for picking the strongest move
│   └── cli.py          # User input/output
├── tests/
│   ├── test_api.py
│   ├── test_cli.py
│   └── test_finder.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
```

## How It Works
1. `GET /pokemon/{name}` returns every move the Pokémon can learn (names and URLs only).
2. `GET /move/{name}` is called for each move to read its `power`.
3. Moves with `power: null` are skipped, and the highest power wins.


## Acknowledgments
Data provided by [PokeAPI](https://pokeapi.co). Pokémon and related names are trademarks of
Nintendo, Game Freak, and The Pokémon Company; this project is not affiliated with them.

