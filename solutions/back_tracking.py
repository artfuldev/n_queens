from copy import copy
from functools import partial
from typing import Generator
from models.board import (
    Board,
    RowPair,
    Size,
    Column,
    has_collision,
    row_pairs,
)
from algorithms.back_tracking import back_tracking as algorithm


def __root(_: Size) -> Board | None:
    return Board([])


def __indices(size: Size, board: Board) -> Generator[RowPair, None, None]:
    filled_size = len(board)
    for pair in row_pairs(size):
        x, y = pair
        if x < filled_size and y < filled_size:
            yield pair


def __reject(size: Size, board: Board) -> bool:
    return any(filter(partial(has_collision, board), __indices(size, board)))


def __accept(size: Size, board: Board) -> bool:
    return len(board) == size


def __concat(board: Board, col: Column) -> Board:
    cols = copy(board)
    cols.append(col)
    return cols


def __replace_last(board: Board, col: Column) -> Board:
    cols = copy(board)
    cols[-1] = col
    return cols


def __next(size: Size, board: Board) -> Board | None:
    filled = len(board)
    if filled > size:
        return None
    column = Column(board[-1] + 1)
    board = __replace_last(board, column)
    while len(set(board)) != filled and column < size:
        column = Column(column + 1)
        board = __replace_last(board, column)
    return None if column == size else board


def __first(size: Size, board: Board) -> Board | None:
    return __next(size, __concat(board, Column(-1)))


back_tracking = algorithm(__root, __reject, __accept, __first, __next)
