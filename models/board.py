from copy import copy
from typing import Generator, NewType, Tuple

Size = NewType("Size", int)
Row = NewType("Row", int)
Column = NewType("Column", int)
Board = NewType("Board", list[Column])
RowPair = NewType("RowPair", Tuple[Row, Row])


def place_queen(board: Board, row: Row, column: Column) -> Board:
    next = copy(board)
    next[row] = column
    return Board(next)


def has_collision(board: Board, rows: RowPair) -> bool:
    row_x, row_y = rows
    col_x = board[row_x]
    col_y = board[row_y]
    if col_x == col_y:
        return True
    row_diff = row_x - row_y
    col_diff = col_x - col_y
    return row_diff == col_diff or row_diff == -col_diff


def row_pairs(size: Size) -> Generator[RowPair, None, None]:
    for x in range(size):
        for y in range(size):
            if x != y:
                yield RowPair((Row(x), Row(y)))


def stringify(board: Board):
    size = len(board)
    row_strings = []
    for row in board:
        col_strings = []
        for i in range(size):
            col_strings.append("Q" if i == row else "_")
        row_strings.append("{}\n".format(" ".join(col_strings)))
    return "".join(row_strings)
