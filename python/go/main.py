"""
A file for testing
"""

from board import Board
from sgfmill import sgf

from player import Player

with open("python/go/data/test_territories.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())
root_node = game.get_root()
black_player = Player(root_node.get("PB"), -1)
white_player = Player(root_node.get("PW"), 1)
moves = [node.get_move() for node in game.get_main_sequence()]

board = Board(9, black_player, white_player)

for move in moves:
    if None in move:
        continue
    color, row, col = move[0], move[1][0], move[1][1]
    board.place_move((row, col), -1 if color == "b" else 1)

print(board.count_territories())
board.show_board()
