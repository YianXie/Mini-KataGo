"""
A simple MiniMax algorithm for Go
"""

from mini_katago.board import Board, Player, Move
import math
import copy

INFINITY = math.inf
player1, player2 = Player("Max Player", -1), Player("Min Player", 1)
board = Board(9, player1, player2)


def game_is_over(board: Board, player: Player) -> bool:
    """
    Check if the game is over by checking if the player has any valid move remaining

    Args:
        player (Player): the player to check

    Returns:
        bool: True if the game is over, False otherwise
    """
    for row in board:
        for move in row:
            if not move.is_empty():
                continue
            move.set_color(player.get_color())
            if board.move_is_valid(move):
                move.set_color(0)
                return False
            move.set_color(0)
    return True


def evaluate(board: Board) -> int:
    """
    Evaluate the current game board by comparing the two players' capture count

    Args:
        board (Board): the game board

    Returns:
        int: the score based on the evaluation
    """
    black_captures, white_captures = (
        board.get_black_player().capture_count,
        board.get_white_player().capture_count,
    )
    if black_captures > white_captures:
        return 1
    elif black_captures < black_captures:
        return -1
    return 0


def get_legal_moves(board: Board, player: Player) -> list[Move]:
    """
    Get all legal moves for a given player

    Args:
        board (Board): the board to check
        player (Player): the player to get all legal moves with

    Returns:
        list[Move]: all legal moves for the given player
    """
    moves: list[Move] = []
    for row in board:
        for move in row:
            if not move.is_empty():
                continue
            move.set_color(player.get_color())
            if board.move_is_valid(move):
                moves.append(move)
            move.set_color(0)
    return moves


def minimax(board: Board, depth: int, isMax: bool) -> int:
    """
    A minimax function the value of a given player

    Args:
        board (Board): the board to check
        depth (int): the depth of the minimax
        isMax (bool): if it is the max player's turn

    Returns:
        int: the score of the given player
    """
    if depth == 0 or game_is_over(board, player1 if isMax else player2):
        return evaluate(board)

    if isMax:
        best = -INFINITY
        for move in get_legal_moves(board, player1):
            board_copy = copy.deepcopy(board)
            board_copy.place_move(move.get_position(), move.get_color())
            score = minimax(board_copy, depth - 1, False)
            best = max(best, score)
        return best
    else:
        best = INFINITY
        for move in get_legal_moves(board, player2):
            board_copy = copy.deepcopy(board)
            board_copy.place_move(move.get_position(), move.get_color())
            score = minimax(board_copy, depth - 1, True)
            best = min(best, score)
        return best
