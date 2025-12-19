import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
from player import Player
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

    def is_empty(self) -> bool:
        """
        Check if a move is still empty

        Returns:
            bool: True if it is empty, False otherwise
        """
        return self.color == 0

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

    def __init__(self, size: int, black_player: Player, white_player: Player) -> None:
        """
        Initialize the board

        Args:
            size (int): the size of the board
        """
        self.size: int = size
        self.black_player: Player = black_player
        self.white_player: Player = white_player
        self.current_player: Player = black_player
        self.state: list[list[Move]] = [
            [Move(row, col) for col in range(size)] for row in range(size)
        ]
        self.__ko_positions: tuple[int, int] = None

    def get_current_player(self) -> Player:
        """
        Get the current playing player

        Returns:
            Player: the player that is currently playing
        """
        return self.current_player

    def get_move(self, position: tuple[int]) -> Move:
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
        Get the neighbors of a given position (maximum 4, minimum 2)

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

    def get_connected(self, move: Move) -> list[Move]:
        """
        Count how many moves are connected to the given move (including the given move)

        Args:
            move (Move): the move to start counting from

        Returns:
            list: a list of all the connected moves with the same color of the given move
        """
        queue = deque[Move]([move])
        visited = set[Move]([move])
        connected = list[Move]([move])
        while queue:
            queued_move = queue.popleft()
            neighbors = self.get_neighbors(queued_move)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor.get_color() == move.get_color():
                    queue.append(neighbor)
                    connected.append(neighbor)
                    visited.add(neighbor)
        return connected

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

    def move_is_valid(self, move: Move) -> bool:
        """
        Check if a given move is valid

        Args:
            move (Move): the move to check

        Returns:
            bool: True if move is valid, False otherwise
        """
        # Prevent suicide
        if not self.check_captures(move) and self.count_liberties(move) <= 0:
            return False

        # Prevent playing the Ko directly after
        elif move.get_position() == self.__ko_positions:
            return False

        return True

    def check_captures(self, move: Move) -> list:
        captures = []
        for neighbor in self.get_neighbors(move):
            if neighbor.get_color() == move.get_color() * -1:
                if self.count_liberties(neighbor) == 0:
                    group = self.get_connected(neighbor)
                    captures.extend(group)

        # Ensure uniqueness
        return list[Move](set[Move](captures))

    def place_move(self, position: tuple[int], color: int) -> None:
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
        if not self.get_move(position).is_empty():
            raise ValueError(f"Position already occupied: {position}")

        move: Move = self.state[position[0]][position[1]]
        prev_color = move.get_color()
        move.set_color(color)
        if not self.move_is_valid(move):
            move.set_color(prev_color)
            raise ValueError("Illegal move")

        # Clear the previous Ko
        self.__ko_positions = None

        # Calculate captures
        captures: list[Move] = self.check_captures(move)
        self.current_player.increase_capture_count(len(captures))
        for capture in captures:
            row, col = capture.get_position()
            self.state[row][col].set_color(0)

        # Check for Ko
        if (
            len(captures) == 1
            and len(self.get_connected(move)) == 1
            and self.count_liberties(move) == 1
        ):
            self.__ko_positions = captures[0].get_position()

        # Switch the player
        self.current_player = (
            self.black_player
            if self.current_player is self.white_player
            else self.white_player
        )

    def count_territories(self) -> tuple:
        """
        Estimate the territories for black and white player

        Returns:
            tuple: a tuple containing the territories for both side in the format (black, white)
        """
        visited = set[Move]()
        black_territories = white_territories = 0
        for row in self.state:
            for move in row:
                if move in visited:
                    continue
                if move.is_empty():
                    queue = deque[Move]([move])
                    queue_visited = set[Move]([move])
                    queued_neighbor_border_colors = set[int]()
                    empty_moves = 1  # include the move itself
                    while len(queue) > 0:
                        queuedMove = queue.popleft()
                        neighbors = self.get_neighbors(queuedMove)
                        for neighbor in neighbors:
                            if neighbor in queue_visited:
                                continue
                            if not neighbor.is_empty():
                                queued_neighbor_border_colors.add(neighbor.get_color())
                            else:
                                empty_moves += 1
                                queue.append(neighbor)
                            queue_visited.add(neighbor)
                    if (
                        -1 in queued_neighbor_border_colors
                        and 1 not in queued_neighbor_border_colors
                    ):
                        black_territories += empty_moves
                    elif (
                        -1 not in queued_neighbor_border_colors
                        and 1 in queued_neighbor_border_colors
                    ):
                        white_territories += empty_moves
                    visited.update(queue_visited)
                visited.add(move)

        return (black_territories, white_territories)

    def print_ascii_board(self) -> None:
        print()
        for row in self.state:
            for move in row:
                color = move.get_color()
                print("B" if color == -1 else "W" if color == 1 else ".", end=" ")
            print()
        print()

    def show_board(self) -> None:
        """
        Display the board
        """
        fig = plt.figure(figsize=[9, 9])
        fig.patch.set_facecolor((0.85, 0.64, 0.125))
        ax = fig.add_subplot(111)
        ax.set_axis_off()

        for x in range(self.size):
            ax.plot([x, x], [0, self.size - 1], "k")
        for y in range(self.size):
            ax.plot([0, self.size - 1], [y, y], "k")
        ax.set_position([0, 0, 1, 1])

        for row in self.state:
            for move in row:
                if move.is_empty():
                    continue
                moveRow, moveCol = move.get_position()
                color = "black" if move.get_color() == -1 else "white"

                circle = patches.Circle(
                    (moveCol, self.size - moveRow - 1),
                    radius=0.4,
                    color=color,
                    zorder=3,
                )
                ax.add_patch(circle)

        ax.set_aspect("equal", adjustable="box")
        plt.show()
