from random import shuffle
from board_utils import colliding_indices, place_queen, swap


class Board:
    def __init__(self, size: int = None, rows: list[int] = None, shuffled=False):
        """Return a board of specified size > 3, or the specified rows
        (positions of queens in each row), after optionally shuffling them. The
        size parameter is ignored if rows are provided."""
        if size is None and rows is None:
            raise
        if rows is not None:
            if not isinstance(rows, list):
                raise
            size = len(rows)
            if size <= 3:
                raise
            if any(row >= size or row < 0 or not isinstance(row, int) for row in rows):
                raise
            self.__rows = rows
            self.__size = len(rows)
        else:
            if not isinstance(size, int):
                raise
            if size <= 3:
                raise
            self.__size = size
            self.__rows = [row for row in range(size)]
        if shuffled:
            shuffle(self.__rows)
        self.__colliding_indices = colliding_indices(self.__rows, self.__size)

    def size(self):
        return self.__size

    def collisions(self):
        return len(self.__colliding_indices)

    def is_valid_until(self, row: int):
        def until_row(index):
            x, y = index
            return x <= row and y <= row

        return len(list(filter(until_row, self.__colliding_indices))) == 0

    def is_valid(self):
        return self.collisions() == 0

    def queen(self, row: int):
        return self.__rows[row]

    def __stringify_row(self, row: int):
        col_strings = []
        for i in range(self.__size):
            col_strings.append("Q" if i == row else "_")
        return " ".join(col_strings)

    def stringify(self):
        row_strings = []
        for row in self.__rows:
            row_strings.append(self.__stringify_row(row))
        return "\n".join(row_strings) + "\n"

    def place(self, row: int, col: int):
        return Board(rows=place_queen(self.__rows, row, col))
    
    def swap(self, row_x: int, row_y: int):
        return Board(rows=(swap(self.__rows, row_x, row_y)))
