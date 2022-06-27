from functools import partial
from itertools import islice
from typing import Generator, NewType, Tuple
from models.board import (
    Board,
    RowPair,
    Size,
    Row,
    Column,
    has_collision,
    row_pairs,
    place_queen,
)
from algorithms.back_tracking import back_tracking as algorithm

Candidate = NewType("Candidate", Tuple[Row, Column, Board])


def __row(candidate: Candidate) -> Row:
    row, *_ = candidate
    return row


def __column(candidate: Candidate) -> Column:
    _, column, *_ = candidate
    return column


def __board(candidate: Candidate) -> Board:
    *_, board = candidate
    return board


def __root(size: Size) -> Candidate:
    return Candidate((Row(-1), Column(0), Board([Column(0) for _ in range(size)])))


def __indices(size: Size, candidate: Candidate) -> Generator[RowPair, None, None]:
    row = __row(candidate)
    for pair in row_pairs(size):
        x, y = pair
        if x <= row and y <= row:
            yield pair


def __reject(size: Size, candidate: Candidate) -> bool:
    reject = any(
        filter(partial(has_collision, __board(candidate)), __indices(size, candidate))
    )
    return reject


def __accept(size: Size, candidate: Candidate) -> bool:
    accept = __row(candidate) == size - 1
    return accept


def __first(size: Size, candidate: Candidate) -> Candidate:
    row = Row(__row(candidate) + 1)
    column = Column(0)
    board = place_queen(__board(candidate), row, column)
    while len(set(islice(board, row + 1))) != row + 1:
        column = Column(column + 1)
        board = place_queen(__board(candidate), row, column)
    first = Candidate((row, column, board))
    return first


def __next(size: Size, candidate: Candidate) -> Candidate | None:
    row = __row(candidate)
    column = Column(__column(candidate) + 1)
    next = None
    board = place_queen(__board(candidate), row, column)
    while len(set(islice(board, row + 1))) != row + 1 and column != size:
        column = Column(column + 1)
        board = place_queen(__board(candidate), row, column)
    if column != size:
        next = Candidate((row, column, board))
    return next


def __output(size: Size, candidate: Candidate):
    return __board(candidate)


back_tracking = algorithm(__root, __reject, __accept, __output, __first, __next)
