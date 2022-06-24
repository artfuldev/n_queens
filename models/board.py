from copy import copy
from typing import Generator, NewType, Tuple

Size = NewType("Size", int)
Row = NewType("Row", int)
Column = NewType("Column", int)
Board = NewType("Board", list[Column])
Index = NewType("Index", Tuple[Row, Column])


def place_queen(board: Board, row: Row, column: Column) -> Board:
    next = copy(board)
    next[row] = column
    return Board(next)


def has_collision(board: Board, index: Index) -> bool:
    x, y = index
    x_queen = board[x]
    y_queen = board[y]
    if x_queen == y_queen:
        return True
    row_diff = x - y
    col_diff = x_queen - y_queen
    return row_diff == col_diff or row_diff == -col_diff


def indices(size: Size) -> Generator[Index, None, None]:
    for x in range(size):
        for y in range(size):
            if x != y:
                yield Index([Row(x), Column(y)])


def stringify(board: Board):
    size = len(board)
    row_strings = []
    for row in board:
        col_strings = []
        for i in range(size):
            col_strings.append("Q" if i == row else "_")
        row_strings.append("{}\n".format(" ".join(col_strings)))
    return "".join(row_strings)
