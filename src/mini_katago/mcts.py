"""
A pure Monte Carlo Tree Search algorithm for Go
"""

import copy
import math
import random
from typing import Self

# fmt: off
from mini_katago.board import Board, Move
from mini_katago.constants import (EXPLORATION_CONSTANT, INFINITY,
                                   MAX_GAME_DEPTH, NUM_SIMULATIONS)
from mini_katago.player import Player

# fmt: on


black_player, white_player = Player("Black Player", -1), Player("White Player", 1)
black_player.opponent, white_player.opponent = white_player, black_player
board = Board(9, black_player, white_player)
color = -1


class Node:
    """
    A node represents a game state (board position).
    """

    def __init__(
        self,
        visits: int,
        total_wins: int,
        player_to_play: Player,
        parent: Self | None,
        move_from_parent: Move | None,
    ) -> None:
        """
        Initialize a node object

        Args:
            visits (int): the amount of visits that the node has
            total_wins (int): the accumulated wins of this node
            player_to_play (Player): the player that is about to play next
            parent (Self | None): pointer to the previous node, root has None
            move_from_parent (Move | None): the parent move that leads to this node, root has None
        """
        self.visits = visits
        self.total_wins = total_wins
        self.player_to_play = player_to_play
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.untried_moves: list[Move] | None = None
        self.children: dict[Move, Self] | None = {}

    def uct_score(self, parent_visits: int, C: float = EXPLORATION_CONSTANT) -> float:
        """
        Calculate the UCT (Upper Confidence Bounds applied to tree) score

        Args:
            parent_visits (int): the node's parent's visits
            C (float, optional): the exploration constant, normally between 1.2-2. Defaults to 1.5.

        Returns:
            float: the UCT score
        """
        if self.visits == 0:
            return INFINITY
        return self.total_wins / self.visits + C * math.sqrt(
            math.log(max(1, parent_visits))  # uses max(1, parent_visits) as a safeguard
            / self.visits
        )

    def select_child(self) -> Self | None:
        """
        Return the child with the highest UCT score

        Returns:
            Self | None: the child with the highest UCT score, or None if node has no children
        """
        best_score = -INFINITY
        best_node: Self | None = None
        if self.children:
            for node in self.children.values():
                score = node.uct_score(node.parent.visits)  # type: ignore
                if score > best_score:
                    best_score = score
                    best_node = node
            return best_node
        return None

    def select_move(self) -> Move | None:
        """
        Return the child move with the highest UCT score

        Returns:
            Move | None: the child move with the highest UCT score, or None if node has no children
        """
        best_score = -INFINITY
        best_move: Move | None = None
        if self.children:
            for move, node in self.children.items():
                score = node.uct_score(node.parent.visits)  # type: ignore
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move
        return None

    def __repr__(self) -> str:
        """
        Return a developer-friendly message for debugging

        Returns:
            str: a developer friendly message
        """
        return f"visits: {self.visits}, total_wins: {self.total_wins}, player_to_player: {self.player_to_play}, parent: {self.parent}, move_from_parent: {self.move_from_parent}"


def mcts(root_board: Board, root_player: Player) -> Move:
    root = Node(
        visits=0,
        total_wins=0,
        player_to_play=root_player,
        parent=None,
        move_from_parent=None,
    )
    root.untried_moves = root_board.get_legal_moves(root_player.get_color())

    for _ in range(NUM_SIMULATIONS):
        board = copy.deepcopy(root_board)
        node = root
        player = root_player

        # 1) Selection
        while not node.untried_moves and not board.is_terminate() and node.children:
            temp_node = node.select_child()
            if temp_node is None:
                break
            node = temp_node
            board.place_move(
                node.move_from_parent.get_position(),  # type: ignore
                node.player_to_play.get_color(),
            )
            player = player.opponent

        # 2) Expansion (add 1 child)
        if not board.is_terminate():
            # Attempt to get legal moves if it not already exists
            if node.untried_moves is None:
                node.untried_moves = board.get_legal_moves(player.get_color())

            if node.untried_moves:
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)

                board.place_move(move.get_position(), player.get_color())
                child = Node(
                    visits=0,
                    total_wins=0,
                    player_to_play=player.opponent,
                    parent=node,
                    move_from_parent=move,
                )
                player = player.opponent
                child.untried_moves = board.get_legal_moves(player.get_color())
                node.children[move] = child  # type: ignore
                node = child

        # 3) Simulation (rollout)
        rollout_player = player
        depth = 0
        while not board.is_terminate() and depth < MAX_GAME_DEPTH:
            moves = board.get_legal_moves(rollout_player.get_color())
            if not moves:
                board.pass_move()
                rollout_player = rollout_player.opponent
                continue

            move = random.choice(moves)
            board.place_move(move.get_position(), rollout_player.get_color())

            rollout_player = rollout_player.opponent
            depth += 1

        # 4) Back-propagation
        black_score, white_score = board.calculate_score()
        while node is not None:
            node.visits += 1
            # From the root player's perspective
            root_won = (
                (black_score > white_score)
                if root_player.get_color() == -1
                else (white_score > black_score)
            )
            node.total_wins += int(root_won)
            node = node.parent  # type: ignore

    best: Node = list(root.children.values())[0]  # type: ignore
    for value in root.children.values():  # type: ignore
        if value.visits > best.visits:
            best = value
    return best.move_from_parent  # type: ignore


while not board.is_terminate():
    row, col = map(int, input("Enter row and col to play: ").split())
    board.place_move((row, col), color)
    color *= -1
    board.print_ascii_board()

    move = mcts(board, white_player)
    print(move)
    board.place_move(move.get_position(), white_player.get_color())
    color *= -1
    board.print_ascii_board()
