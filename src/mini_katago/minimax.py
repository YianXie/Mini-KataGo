"""
A simple MiniMax algorithm for Go
"""

from mini_katago.board import Board, Player, Move
import math

INFINITY = math.inf

# Here, the min player is black, and the max player is white (MiniMax)
min_player, max_player = Player("Black Player", -1), Player("White Player", 1)
board = Board(9, min_player, max_player)


def game_is_over(board: Board, player: Player) -> bool:
    """
    Check if the game is over by checking if the player has any valid move remaining

    Args:
        player (Player): the player to check

    Returns:
        bool: True if the game is over, False otherwise
    """
    for row in board.state:
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
        int: the score based on the evaluation (positive favors white, negative favors black)
    """
    black_captures, white_captures = (
        board.get_black_player().capture_count,
        board.get_white_player().capture_count,
    )

    # Return the difference: positive means white is ahead, negative means black is ahead
    return white_captures - black_captures


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
    for row in board.state:
        for move in row:
            if not move.is_empty():
                continue
            move.set_color(player.get_color())
            if board.move_is_valid(move):
                moves.append(move)
            move.set_color(0)
    return moves


def minimax(board: Board, depth: int, isMax: bool, alpha: int, beta: int) -> int:
    """
    A depth-limited minimax function the value of a given player

    Args:
        board (Board): the board to check
        depth (int): the depth of the minimax
        isMax (bool): if it is the max player's turn
        alpha (int): the best value guaranteed for the max player
        beta (int): the best value guaranteed for the min player

    Returns:
        int: the score of the given player
    """
    if depth <= 0 or game_is_over(board, max_player if isMax else min_player):
        return evaluate(board)

    if isMax:
        best = -INFINITY
        for move in get_legal_moves(board, max_player):
            board.place_move(move.get_position(), max_player.get_color())
            score = minimax(board, depth - 1, False, alpha, beta)
            board.undo()
            best = max(best, score)
            alpha = max(alpha, best)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return best

    else:
        best = INFINITY
        for move in get_legal_moves(board, min_player):
            board.place_move(move.get_position(), min_player.get_color())
            score = minimax(board, depth - 1, True, alpha, beta)
            board.undo()
            best = min(best, score)
            beta = min(beta, best)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return best


def next_best_move(board: Board, isMax: bool) -> Move:
    """
    Find the next best move for the given player

    Args:
        board (Board): the board to check
        isMax (bool): if it is the max player's turn

    Returns:
        Move: the next best move for the given player
    """
    best_score = -INFINITY if isMax else INFINITY
    best_move = None

    for move in get_legal_moves(board, max_player if isMax else min_player):
        board.place_move(
            move.get_position(),
            max_player.get_color() if isMax else min_player.get_color(),
        )
        score = minimax(board, 2, not isMax, -INFINITY, INFINITY)
        board.undo()
        if (isMax and score > best_score) or (not isMax and score < best_score):
            best_score = score
            best_move = move

    return best_move


if __name__ == "__main__":
    while True:
        row, col = map(int, input("Enter a position to place your move: ").split())
        if row == -1 or col == -1:
            break
        board.place_move((row, col), min_player.get_color())
        board.print_ascii_board()

        move = next_best_move(board, isMax=True)
        if move is not None:
            board.place_move(move.get_position(), max_player.get_color())
            board.print_ascii_board()

    board.show_board()
