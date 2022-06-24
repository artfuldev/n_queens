from copy import copy
from functools import partial
from models.board import Board, has_collision, indices
from algorithms.brute_force import brute_force as algorithm


def __next_permutation(board: Board) -> Board:
    rows = copy(board)
    r = len(rows) - 1
    while rows[r - 1] >= rows[r] and r > 0:
        r -= 1
    pivot = r
    if pivot == 0:
        rows.sort()
        return rows
    else:
        swap = len(rows) - 1
        while rows[pivot - 1] >= rows[swap] and swap >= 0:
            swap -= 1
        rows[pivot - 1], rows[swap] = rows[swap], rows[pivot - 1]
        rows[pivot:] = sorted(rows[pivot:])
    return rows


def __first(size: int) -> Board:
    return list(range(size))


def __next(size: int, board: Board) -> Board | None:
    next = __next_permutation(board)
    return None if next == list(range(size)) else next


def __accept(size: int, board: Board) -> bool:
    return not any(filter(partial(has_collision, board), indices(size)))


brute_force = algorithm(__first, __next, __accept)
