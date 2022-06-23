from board_utils import colliding_indices, empty, filled, place_queen


class Board:
    @classmethod
    def empty(cls, size):
        return Board(empty(size))

    @classmethod
    def random(cls, size):
        return Board(filled(size))

    def __init__(self, rows):
        self.__size = len(rows)
        self.__rows = rows
        self.__colliding_indices = colliding_indices(self.__rows, self.__size)

    def size(self):
        return self.__size

    def collisions(self):
        return len(self.__colliding_indices)

    def is_valid(self):
        return self.collisions() == 0

    def queen(self, row):
        return self.__rows[row]

    def __stringify_row(self, row):
        col_strings = []
        for i in range(self.__size):
            col_strings.append("Q" if i == row else "_")
        return " ".join(col_strings)

    def stringify(self):
        row_strings = []
        for row in self.__rows:
            row_strings.append(self.__stringify_row(row))
        return "\n".join(row_strings) + "\n"

    def place(self, row, col):
        return Board(place_queen(self.__rows, row, col))
