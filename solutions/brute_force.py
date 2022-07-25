from copy import copy
from functools import partial
from typing import Optional

from domain.board import Board, Column, Size, create, from_list, has_collision, row_pairs, to_list
from algorithms.brute_force import brute_force as algorithm


def __next_permutation(board: Board) -> Board:
    columns = to_list(board)
    r = len(columns) - 1
    while columns[r - 1] >= columns[r] and r > 0:
        r -= 1
    pivot = r
    if pivot == 0:
        columns.sort()
        return from_list(columns)
    else:
        swap = len(columns) - 1
        while columns[pivot - 1] >= columns[swap] and swap >= 0:
            swap -= 1
        columns[pivot - 1], columns[swap] = columns[swap], columns[pivot - 1]
        columns[pivot:] = sorted(columns[pivot:])
    return from_list(columns)


def __first(size: Size) -> Optional[Board]:
    return create(size) if size > 3 else None


def __next(size: Size, board: Board) -> Optional[Board]:
    next = __next_permutation(board)
    return None if next == __first(size) else next


def __accept(size: Size, board: Board) -> bool:
    return not any(filter(partial(has_collision, board), row_pairs(size)))


def __output(_: Size, board: Board) -> Board:
    return board


brute_force = algorithm(__first, __next, __accept, __output)
