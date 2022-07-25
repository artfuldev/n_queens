from functools import partial
from random import shuffle
from typing import Generator, Tuple
from pyrsistent import pvector
from pyrsistent.typing import PVector

Size = int
Row = int
Column = int
Board = PVector[Column]


def from_list(columns: list[Column]) -> Board:
    return pvector(columns)


def to_list(board: Board) -> list[Column]:
    return list(iter(board))


def create(n: Size) -> Board:
    return from_list(list(range(n)))


def permute(board: Board) -> Board:
    columns = to_list(board)
    shuffle(columns)
    return from_list(columns)


def shuffled(n: Size) -> Board:
    return permute(create(n))


def place_queen(board: Board, row: Row, column: Column) -> Board:
    return board.set(row, column)


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


def swap(board: Board, x: Row, y: Row) -> Board:
    return board.set(y, board[x]).set(x, board[y])


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
