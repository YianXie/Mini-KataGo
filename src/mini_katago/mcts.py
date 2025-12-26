"""
A pure Monte Carlo Tree Search algorithm for Go
"""

import copy
import random
from collections import defaultdict
from mini_katago.board import Board, Move
from mini_katago.player import Player


SIMULATIONS = 500
MAX_DEPTH = 50

black_player, white_player = Player("Black Player", -1), Player("White Player", 1)
board = Board(9, black_player, white_player)


def next_best_move(board: Board, player: Player):
    """
    Get the next best move by playing random moves and calculate win rates

    Args:
        board (Board): the board state
        player (Player): the player that is playing
    """
    # The first element in the tuple represents the total games played, the second element represents the amount of games won
    win_rates = defaultdict[Move, list[int]](lambda: [0, 0])
    for _ in range(SIMULATIONS):
        board_copy = copy.deepcopy(board)
        depth = 0
        color = player.get_color()
        while True:
            depth += 1
            legal_moves: list[Move] = board_copy.get_legal_moves(color)
            if legal_moves:
                random_move = random.choice(legal_moves)
                board_copy.place_move(random_move.get_position(), color)
                if board_copy.is_terminate() or depth >= MAX_DEPTH:
                    win_rates[random_move][0] += 1
                    scores = board_copy.calculate_score()
                    if (player.get_color() == -1 and scores[0] > scores[1]) or (
                        player.get_color() == 1 and scores[0] < scores[1]
                    ):
                        win_rates[random_move][1] += 1
                        break
            else:
                break

            color *= -1

    best_win_rate: float = 0
    best_move: Move | None = None
    for move, win_rate in win_rates.items():
        if win_rate[1] / win_rate[0] > best_win_rate:
            best_win_rate = win_rate[1] / win_rate[0]
            best_move = move

    return best_move


while not board.is_terminate():
    row, col = map(int, input("Enter your move: ").strip().split())
    board.place_move((row, col), black_player.get_color())
    board.print_ascii_board()

    move = next_best_move(board, black_player)
    board.place_move(move.get_position(), white_player.get_color())
    board.print_ascii_board()
