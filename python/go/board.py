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
        self.state = [[0] * size for _ in range(size)]

    def is_valid_move(self, position) -> bool:
        """
        Check if the given position is a valid move

        Args:
            position (tuple): the position of the move

        Returns:
            bool: True if the position is a valid move, False otherwise
        """
        return 0 <= position[0] < self.size and 0 <= position[1] < self.size

    def is_valid_color(self, color) -> bool:
        """
        Check if the given color is a valid color

        Args:
            color (int): the color of the move

        Returns:
            bool: True if the color is a valid color, False otherwise
        """
        return color in [-1, 1]

    def get_move(self, position) -> int:
        """
        Get the move at the given position

        Args:
            position (tuple): the position of the move

        Returns:
            int: the color of the move at the given position
        """
        if not self.is_valid_move(position):
            raise ValueError(f"Invalid position: {position}")
        return self.state[position[0]][position[1]]

    def get_neighbors(self, position) -> list:
        """
        Get the neighbors of a given position

        Args:
            position (tuple): the position of the move

        Returns:
            set: a set of the neighbors of the given position
        """
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

    def count_liberties(self, position) -> int:
        """
        Count the liberties of a given position

        Args:
            position (tuple): the position of the move

        Returns:
            int: the amount of liberties of that position
        """
        color = self.get_move(position)
        if color == 0:
            return -1
        neighbors = self.get_neighbors(position)
        liberties = len(neighbors)
        for neighbor in neighbors:
            liberties -= int(neighbor != 0)
        return liberties

    def check_captures(self, position) -> set:
        """
        Check if the given position is a capture

        Args:
            position (tuple): the position of the move

        Returns:
            set: a set of positions that are captured
        """
        print(self.count_liberties(position))

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
        if not self.is_valid_move(position):
            raise ValueError(f"Invalid position: {position}")
        if not self.is_valid_color(color):
            raise ValueError(f"Invalid color: {color}")
        if self.get_move(position) != 0:
            raise ValueError(f"Cannot place move at {position}: already occupied")
        self.state[position[0]][position[1]] = color

        # Calculate captures
        self.check_captures(position)

    def print_board(self) -> None:
        """
        Print the board
        """
        print()
        for row in self.state:
            for cell in row:
                print("W" if cell == 1 else "B" if cell == -1 else ".", end=" ")
            print()
        print()
