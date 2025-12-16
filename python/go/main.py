from board import Board

board = Board(9)

board.place_move((0, 1), -1)
board.place_move((0, 0), 1)
board.place_move((3, 1), -1)
board.place_move((3, 3), -1)
board.place_move((3, 2), 1)

board.print_board()
