"""
A pure Monte Carlo Tree Search algorithm for Go
"""

import math
import random
from collections import defaultdict
from mini_katago.board import Board, Move
from mini_katago.player import Player


class Node:
    """
    A node class represents a root move
    """

    EXPLORATION_CONSTANT = 1.5

    def __init__(
        self, visits: int, value: int, untried_moves: list[Move], player_to_play: Player
    ) -> None:
        """
        Initialize a node object

        Args:
            visits (int): the amount of visits that the node has
            value (int): the value of this node (-1, 0, or 1), represents win/lose/tie
            untried_moves (list[Move]): all of the legal moves available at this move
            player_to_play (Player): the player that is about to play next
        """
        self.visits = visits
        self.value = value
        self.untried_moves = untried_moves
        self.player_to_play = player_to_play
        self.child = None

    def uct_score(self, parent_visits: int, C: float = EXPLORATION_CONSTANT) -> float:
        """
        Calculate the UCT (Upper Confidence Bounds applied to tree) score

        Args:
            parent_visits (int): the node's parent's visits
            C (float, optional): the exploration constant, normally between 1.2-2. Defaults to EXPLORATION_CONSTANT (1.5).

        Returns:
            float: the UCT score
        """
        return self.value / self.visits + C * math.sqrt(
            math.log(parent_visits) / self.visits
        )


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
        depth = 0
        total_moves = 1  # start from 1 because of the root move
        color = player.get_color()
        root_move = random.choice(board.get_legal_moves(color))
        board.place_move(root_move.get_position(), player.get_color())
        while True:
            depth += 1
            legal_moves: list[Move] = board.get_legal_moves(color)
            if legal_moves:
                random_move = random.choice(legal_moves)
                total_moves += 1
                board.place_move(random_move.get_position(), color)
                if board.is_terminate() or depth >= MAX_DEPTH:
                    win_rates[root_move][0] += 1
                    scores = board.calculate_score()
                    if (player.get_color() == -1 and scores[0] > scores[1]) or (
                        player.get_color() == 1 and scores[0] < scores[1]
                    ):
                        win_rates[root_move][1] += 1
                        break
            else:
                board.pass_move()  # pass if no legal moves available

            color *= -1

        # Undo all moves
        for _ in range(total_moves):
            board.undo()

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
