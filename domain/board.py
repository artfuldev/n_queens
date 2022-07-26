from functools import partial
from random import choice, randint, shuffle
from typing import Generator, Optional, Tuple, cast
from pyrsistent import pvector
from pyrsistent.typing import PVector

from domain.list import flatten, unique

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


def shuffled(n: Size) -> Board:
    columns = to_list(create(n))
    shuffle(columns)
    return from_list(columns)


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


def random_row_pair(n: Size) -> Tuple[Row, Row]:
    x = randint(0, n - 1)
    y = randint(0, n - 1)
    while x == y:
        y = randint(0, n - 1)
    return (Row(x), Row(y))


def colliding_row_pairs(n: Size, board: Board) -> list[Tuple[Row, Row]]:
    return list(filter(partial(has_collision, board), row_pairs(n)))


def collisions(n: Size, board: Board) -> int:
    return len(colliding_row_pairs(n, board))


def random_row_pair_that_may_reduce_collisions(
    n: Size, board: Board
) -> Optional[Tuple[Row, Row]]:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return None
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    return None if len(y_choices) == 0 else (x, choice(y_choices))


def swap(board: Board, x: Row, y: Row) -> Board:
    return board.set(y, board[x]).set(x, board[y])


def swap_rows(board: Board, rows: Tuple[Row, Row]) -> Board:
    x, y = rows
    return swap(board, x, y)


def cache_key(board: Board) -> str:
    return ",".join(map(str, board))


def stringify(board: Board):
    size = len(board)
    row_strings = []
    for row in board:
        col_strings = []
        for i in range(size):
            col_strings.append("Q" if i == row else "_")
        row_strings.append("{}\n".format(" ".join(col_strings)))
    return "".join(row_strings)
