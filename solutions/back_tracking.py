from typing import Optional

from domain.board import (
    Board,
    Size,
    from_list,
    has_collision,
    place_queen,
    row_pairs,
)
from algorithms.back_tracking import back_tracking as algorithm


def __root(_: Size) -> Optional[Board]:
    return from_list([])


def __reject(size: Size, board: Board) -> bool:
    filled_size = len(board)
    for pair in row_pairs(size):
        x, y = pair
        if x < filled_size and y < filled_size and has_collision(board, pair):
            return True
    return False


def __accept(size: Size, board: Board) -> bool:
    return len(board) == size


def __next(size: Size, board: Board) -> Optional[Board]:
    filled = len(board)
    if filled > size:
        return None
    row = filled - 1
    column = board[-1] + 1
    while column < size:
        board = place_queen(board, row, column)
        if len(set(board)) == filled:
            return board
        column += 1
    return None


def __first(size: Size, board: Board) -> Optional[Board]:
    return __next(size, board.append(-1))


def __output(_: Size, board: Board) -> Board:
    return board


back_tracking = algorithm(__root, __reject, __accept, __first, __next, __output)
