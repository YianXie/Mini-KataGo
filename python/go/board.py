from collections import deque
from rules import Rules


class Move:
    """
    A class representing a move
    """

    def __init__(self, row=-1, col=-1, color=0) -> None:
        """
        Initialize the move

        Args:
            row (int, optional): the row of the move. Defaults to -1.
            col (int, optional): the column of the move. Defaults to -1.
            color (int, optional): the color of the move. Defaults to 0.
        """
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, position) -> None:
        """
        Set the position of the move

        Args:
            position (tuple): the position of the move

        Raises:
            ValueError: if the position is invalid
        """
        if not Rules.position_is_valid(position):
            raise ValueError(f"Invalid position: {position}")
        self.position = position

    def set_color(self, color) -> None:
        """
        Set the color of the move

        Args:
            color (int): the color of the move

        Raises:
            ValueError: if the color is invalid
        """
        if not Rules.color_is_valid(color):
            raise ValueError(f"Invalid color: {color}")
        self.color = color

    def get_position(self) -> tuple:
        """
        Get the position of the move

        Returns:
            tuple: the position of the move
        """
        return (self.row, self.col)

    def get_color(self) -> int:
        """
        Get the color of the move

        Returns:
            int: the color of the move
        """
        return self.color

    def __repr__(self):
        """
        Return a developer-friendly message

        Returns:
            str: a message that describes the move
        """
        return f"(({self.row}, {self.col}), {self.color})"


class Board:
    """
    A class representing a Go board

    Colors:
        -1: Black
        0: Empty
        1: White
    """

    def __init__(self, size) -> None:
        """
        Initialize the board

        Args:
            size (int): the size of the board
        """
        self.size = size
        self.state: list[list[Move]] = []
        for row in range(size):
            self.state.append([])
            for col in range(size):
                self.state[row].append(Move(row, col))

    def get_move(self, position) -> Move:
        """
        Get the move at the given position

        Args:
            position (tuple): the position of the move

        Returns:
            Move: the move at the given position
        """
        if not Rules.position_is_valid(position):
            raise ValueError(f"Invalid position: {position}")
        return self.state[position[0]][position[1]]

    def get_neighbors(self, move: Move) -> list[Move]:
        """
        Get the neighbors of a given position

        Args:
            move (Move): the move

        Returns:
            list: a list of the neighbors of the given position
        """
        position = move.get_position()
        neighbors = []
        if position[0] - 1 >= 0:
            neighbors.append(self.get_move((position[0] - 1, position[1])))
        if position[0] + 1 < self.size:
            neighbors.append(self.get_move((position[0] + 1, position[1])))
        if position[1] - 1 >= 0:
            neighbors.append(self.get_move((position[0], position[1] - 1)))
        if position[1] + 1 < self.size:
            neighbors.append(self.get_move((position[0], position[1] + 1)))
        return neighbors

    def count_liberties(self, move: Move) -> int:
        """
        Iterative solution to count the liberties of a given position

        Args:
            move (Move): the move

        Returns:
            int: the amount of liberties of that position, -1 if move is empty
        """
        color = move.get_color()
        if color == 0:
            return -1

        liberties = 0
        queue = deque[Move]([move])
        visited = set[Move]([move])
        while len(queue) > 0:
            queuedMove = queue.popleft()
            neighbors = self.get_neighbors(queuedMove)
            for neighbor in neighbors:
                neighborColor = neighbor.get_color()
                if neighborColor == color and neighbor not in visited:
                    queue.append(neighbor)
                elif neighborColor == 0 and neighbor not in visited:
                    liberties += 1
                visited.add(neighbor)

        return liberties

    def check_captures(self, move: Move) -> list:
        """
        Check if the given position is a capture

        Args:
            move (Move): the move

        Returns:
            list: a list of positions that are captured
        """
        captures = []
        queue = deque[Move]([move])
        visited = set[Move]([move])
        while len(queue) > 0:
            queuedMove = queue.popleft()
            neighbors = self.get_neighbors(queuedMove)
            for neighbor in neighbors:
                if neighbor.get_color() == 0:
                    continue
                if neighbor.get_color() == move.get_color() and neighbor not in visited:
                    queue.append(neighbor)
                elif (
                    neighbor.get_color() == move.get_color() * -1
                    and neighbor not in visited
                ):
                    if self.count_liberties(neighbor) == 0:
                        captures.append(neighbor)
                        queue.append(neighbor)
                visited.add(neighbor)
        return captures

    def move_is_valid(self, move: Move) -> bool:
        """
        Check if a given move is invalid

        Args:
            move (Move): the move

        Returns:
            bool: True if is invalid, False otherwise
        """
        if self.count_liberties(move) <= 0:
            return False
        return True

    def place_move(self, position, color) -> None:
        """
        Place a move on the board

        Args:
            position (tuple): the position of the move
            color (int): the color of the move

        Raises:
            ValueError: if the position is invalid
            ValueError: if the color is invalid
            ValueError: if the position is already occupied
        """
        if not Rules.position_is_valid(position):
            raise ValueError(f"Invalid position: {position}")
        if not Rules.color_is_valid(color):
            raise ValueError(f"Invalid color: {color}")

        prev = self.state[position[0]][position[1]].get_position()
        move: Move = self.state[position[0]][position[1]]
        move.set_color(color)
        if not self.move_is_valid(move):
            move.set_color(prev)
            raise ValueError(f"Illegal move: {position}")

        # Calculate captures
        captures = self.check_captures(move)
        print(f"Captures: {captures}")

    def print_board(self) -> None:
        """
        Print the board
        """
        print()
        for row in self.state:
            for move in row:
                color = move.get_color()
                print("W" if color == 1 else "B" if color == -1 else ".", end=" ")
            print()
        print()
