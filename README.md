# Mini-KataGo

My own implementation of Go AI, similar to [KataGo](https://github.com/lightvector/KataGo).

## Timeline

### Week 1

Implemented basic Go board engine and a simple minimax file for tac-tac-toe that will be later used for Go as a depth-limited MiniMax (and probably see it fails badly)

New features include:

-   Place move at specific position with specific color
-   Captures detection
-   Ko detection
-   Score estimation at the end of the game
-   Illegal move detection
-   Display a real Go board with MatPlotLib

### Week 2

Implemented a basic depth-limited MiniMax algorithm for Go with alpha-beta pruning. It checks all possible moves in a given board state and choose the local optimal one by choosing the move that captures the most opponent's stones. Also did some minor updates to the board class.

New features include:

-   Depth-limited Minimax algorithm with alpha-beta pruning
-   Auto game-over when there are 2 consecutive passes
-   Undo feature for game board

## File structure

```
mini-katago/
├── src/                        # All Python files
│   ├── mini_katago/            # Go related files
│   │   │── __init__.py
│   │   │── board.py            # A file that represents the Go game board
│   │   │── main.py             # A file for testing
│   │   │── player.py           # A file representing the player
│   │   │── rules.py            # A file that contains some basic rules for Go
│   │   │── minimax.py          # A simple depth-limited minimax algorithm for Go
├── tests/                      # All unit-tests
    ├── test_board_rules.py     # Test if board rules works correctly
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

## Development

To start developing this project locally. Run the following command:

```bash
git clone https://github.com/YianXie/Mini-KataGo  # Clone this repository
cd Mini-KataGo
python -m venv venv  # Create a Python virtual environment
source venv/bin/activate  # Activate the virtual environment
which pip  # (optional) confirm that you are using the correct pip
pip install -r requirements.txt  # Install dependencies
```

Now you are ready to start developing. To see a quick demo, you may go the `main.py` and try a few different .sgf files or play your own.

Happy developing!

## Tests

This project contains some tests that you can run while developing to make sure everything works as expected.

To run tests:

```bash
pip install -r requirements.txt  # Install dependencies
```

```bash
pip install -e .  # IMPORTANT: run at root level, otherwise Pytest would not work
```

```bash
pytest  # Run at root level. This would run all tests.
```

To add more tests, simply add a new Python file in the `tests/` directory. Note that it must start with `test_xxx` or `xxx_test`
