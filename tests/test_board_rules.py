import pytest
from mini_katago.board import Board

B, W = -1, 1


def test_single_stone_capture():
    board = Board(9)

    # Place 3 black pieces
    board.place_move((1, 1), B)
    board.place_move((2, 0), B)
    board.place_move((3, 1), B)

    # Place 1 white piece at (2, 1) so it has only 1 liberty
    board.place_move((2, 1), W)
    assert board.get_move((2, 1)).get_color() == W

    # Place 1 black piece to capture the white piece
    board.place_move((2, 3), B)

    assert board.get_move((2, 2)).is_empty(), "White should be captured"


def test_group_capture():
    board = Board(9)

    # White group: two stones connected horizontally
    board.place_move((2, 2), W)
    board.place_move((2, 3), W)

    # Surround the group with black stones
    black_moves = [
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 4),
        (3, 2),
        (3, 3),
    ]
    for mv in black_moves:
        board.place_move(mv, B)

    assert board.get_move((2, 2)).is_empty()
    assert board.get_move((2, 3)).is_empty()
