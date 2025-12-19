# Mini-KataGo

My own implementation of Go AI, similar to [KataGo](https://github.com/lightvector/KataGo).

## Timeline

### Week 1

Implemented basic Go board engine and a simple minimax file for tac-tac-toe that will be later used for Go as a depth-limited MiniMax (and probably see it fails badly)

Current feature includes:

-   Place move at specific position with specific color
-   Captures detection
-   Ko detection
-   Score estimation at the end of the game
-   Illegal move detection
-   Display a real Go board with MatPlotLib

...

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
│   │   │── minimax.py          # A simple minimax algorithm for tic-tac-toe
├── tests/                      # All unit-tests
    ├── test_board_rules.py     # Test if board rules works correctly
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```
