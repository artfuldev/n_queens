from copy import copy
from models.board import (
    Board,
    Row,
    Size,
    Column,
    has_collision,
    place_queen,
    row_pairs,
)
from algorithms.back_tracking import back_tracking as algorithm


def __root(_: Size) -> Board | None:
    return Board([])


def __reject(size: Size, board: Board) -> bool:
    filled_size = len(board)
    for pair in row_pairs(size):
        x, y = pair
        if x < filled_size and y < filled_size and has_collision(board, pair):
            return True
    return False


def __accept(size: Size, board: Board) -> bool:
    return len(board) == size


def __next(size: Size, board: Board) -> Board | None:
    filled = len(board)
    if filled > size:
        return None
    row = Row(filled - 1)
    column = Column(board[-1] + 1)
    board = place_queen(board, row, column)
    while len(set(board)) != filled and column < size:
        column = Column(column + 1)
        board = place_queen(board, row, column)
    return None if column == size else board


def __first(size: Size, board: Board) -> Board | None:
    seed = copy(board)
    seed.append(Column(-1))
    return __next(size, seed)


back_tracking = algorithm(__root, __reject, __accept, __first, __next)
