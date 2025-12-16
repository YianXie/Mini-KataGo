"""
A simple MiniMax algorithm for tic-tac-toe

-1 - o wins
0 - tie
1 - x wins
"""

import math

INFINITY = math.inf
player, opponent = "x", "o"
board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]


def goal_test(board) -> int:
    """
    A goal-test function that evaluates the current game board

    Args:
        board (list): a 2D array representing the game board

    Returns:
        int: the state of the current board (-1 = 'o' wins, 0 = no one has won, 1 = 'x' wins)
    """

    # Check for row
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "_":
            return 1 if board[row][0] == player else -1

    # Check for column
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "_":
            return 1 if board[0][col] == player else -1

    # Check for positive diagonal
    if board[0][2] == board[1][1] == board[2][0] != "_":
        return 1 if board[0][2] == player else -1

    # Check for negative diagonal
    if board[0][0] == board[1][1] == board[2][2] != "_":
        return 1 if board[0][0] == player else -1

    return 0


def board_is_full(board) -> bool:
    return all(cell != "_" for row in board for cell in row)


def minimax(board, isMax, alpha=-INFINITY, beta=INFINITY) -> int:
    """
    A minimax function with alpha-beta pruning that returns the value for a given player

    Args:
        board (list): a 2D array representing the game board
        isMax (bool): True if maximizing player, False if minimizing
        alpha (float): alpha value for pruning
        beta (float): beta value for pruning

    Returns:
        int: a value representing the best outcome for the given player assume both plays optimally
    """

    currentState = goal_test(board)
    if currentState != 0:
        return currentState
    if board_is_full(board):
        return 0

    if isMax:
        best = -INFINITY
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "x"
                    best = max(best, minimax(board, False, alpha, beta))
                    board[i][j] = "_"
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best
    else:
        best = INFINITY
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "o"
                    best = min(best, minimax(board, True, alpha, beta))
                    board[i][j] = "_"
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best


def next_best_move(board, isMax) -> tuple:
    """
    Determine the estimated next best move based on the current game board

    Args:
        board (list): a 2D array representing the game board
        isMax (bool): True if we want to maximize the player's score

    Returns:
        tuple: the coordinate of the best move
    """

    best_score = -INFINITY if isMax else INFINITY
    best_coords = None
    player_symbol = "x" if isMax else "o"
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = player_symbol
                score = minimax(board, not isMax, -INFINITY, INFINITY)
                if (isMax and score > best_score) or (not isMax and score < best_score):
                    best_score = score
                    best_coords = (i, j)
                board[i][j] = "_"
    
    return best_coords


def print_board(board) -> None:
    """
    print the given game board

    Args:
        board (list): a 2D array representing the game board
    """

    print()
    for row in board:
        for col in row:
            print(col + " ", end="")
        print()
    print()


while True:
    best_move = next_best_move(board, True)
    board[best_move[0]][best_move[1]] = "x"

    print_board(board)

    if goal_test(board) != 0 or board_is_full(board):
        break

    row, col = map(int, input("Enter a coordinate: ").split())
    board[row][col] = "o"

    print_board(board)

    if goal_test(board) != 0 or board_is_full(board):
        break
