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
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == player:
                return 1
            elif board[row][0] == opponent:
                return -1

    # Check for column
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == player:
                return 1
            elif board[0][col] == opponent:
                return -1

    # Check for positive diagonals
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == player:
            return 1
        elif board[0][2] == opponent:
            return -1

    # Check for negative diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == player:
            return 1
        elif board[0][0] == opponent:
            return -1

    return 0


def board_is_full(board) -> bool:
    for row in board:
        for cell in row:
            if cell == "_":
                return False
    return True


def minimax(board, isMax) -> int:
    """
    A minimax function that returns the value for a given player

    Args:
        board (list): a 2D array representing the game board

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
                # If the cell is empty, try it
                if board[i][j] == "_":
                    board[i][j] = "x"
                    best = max(best, minimax(board, not isMax))
                    board[i][j] = "_"
        return best

    else:
        best = INFINITY
        for i in range(3):
            for j in range(3):
                # If the cell is empty, try it
                if board[i][j] == "_":
                    board[i][j] = "o"
                    best = min(best, minimax(board, not isMax))
                    board[i][j] = "_"
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
    if isMax:
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "x"
                    score = minimax(board, not isMax)
                    if score > best_score:
                        best_score = score
                        best_coords = (i, j)
                    board[i][j] = "_"

    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "o"
                    score = minimax(board, not isMax)
                    if score < best_score:
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
