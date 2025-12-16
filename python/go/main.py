"""
A file for testing
"""

from board import Board
from sgfmill import sgf

with open("python/go/data/2.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())
winner = game.get_winner()
board_size = game.get_size()
root_node = game.get_root()
b_player = root_node.get("PB")
w_player = root_node.get("PW")
moves = [node.get_move() for node in game.get_main_sequence()]

board = Board(9)

for move in moves:
    if None in move:
        continue
    color, row, col = move[0], move[1][0], move[1][1]
    board.place_move((row, col), -1 if color == "b" else 1)

board.show_board()
