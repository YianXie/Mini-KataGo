class Rules:
    """
    A class containing rules for a Go game
    """

    @staticmethod
    def position_is_valid(position, size=9) -> bool:
        """
        Check if the given position is valid

        Args:
            position (tuple): the position of the move
            size (int, optional): the size of teh game board. Defaults to 9.

        Raises:
            TypeError: if the position argument is not a tuple

        Returns:
            bool: True if the move is valid, False otherwise
        """
        if not isinstance(position, tuple):
            raise TypeError("Inappropriate position: position must be tuple")
        return 0 <= position[0] < size and 0 <= position[1] < size

    @staticmethod
    def color_is_valid(color) -> bool:
        """
        Check if the given color is a valid color

        Args:
            color (int): the color of the move

        Raises:
            TypeError: if the color argument is not an int

        Returns:
            bool: True if the color is a valid color, False otherwise
        """
        if not isinstance(color, int):
            raise TypeError("Inappropriate color: color must be int")
        return color in [-1, 1]
