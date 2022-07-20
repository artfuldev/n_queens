from copy import copy
from functools import partial
from typing import Generator, NewType, Tuple

Size = NewType("Size", int)
Row = NewType("Row", int)
Column = NewType("Column", int)
Board = NewType("Board", list[Column])


def place_queen(board: Board, row: Row, column: Column) -> Board:
    """returns a new board with a queen placed in the given row and column"""
    next_board = copy(board)
    next_board[row] = column
    return Board(next_board)


def has_collision(board: Board, pair: Tuple[Row, Row]) -> bool:
    row_x, row_y = pair
    col_x = board[row_x]
    col_y = board[row_y]
    if col_x == col_y:
        return True
    row_diff = row_x - row_y
    col_diff = col_x - col_y
    return row_diff == col_diff or row_diff == -col_diff


def row_pairs(size: Size) -> Generator[Tuple[Row, Row], None, None]:
    for x in range(size):
        for y in range(size):
            if x != y:
                yield Row(x), Row(y)

def colliding_row_pairs(n: Size, board: Board) -> list[Tuple[Row, Row]]:
    return list(filter(partial(has_collision, board), row_pairs(n)))

def cache_key(board: Board) -> str:
    return "".join(map(str, board))

def stringify(board: Board):
    size = len(board)
    row_strings = []
    for row in board:
        col_strings = []
        for i in range(size):
            col_strings.append("Q" if i == row else "_")
        row_strings.append("{}\n".format(" ".join(col_strings)))
    return "".join(row_strings)
