"""
A file for testing
"""

from board import Board

board = Board(9)
color = -1

while True:
    row, col = map(int, input("Enter a move: ").split())
    board.place_move((row, col), color)
    color *= -1
    board.print_board()
