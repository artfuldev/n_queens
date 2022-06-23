from models.board import Board
from solvers.brute_force import BruteForceSolver


def __next_permutation(board: Board) -> Board:
    rows = board.rows()
    r = len(rows) - 1
    while rows[r - 1] >= rows[r] and r > 0:
        r -= 1
    pivot = r
    if pivot == 0:
        rows.sort()
        return Board(rows=rows)
    else:
        swap = len(rows) - 1
        while rows[pivot - 1] >= rows[swap] and swap >= 0:
            swap -= 1
        rows[pivot - 1], rows[swap] = rows[swap], rows[pivot - 1]
        rows[pivot:] = sorted(rows[pivot:])
    return Board(rows=rows)


def __first(size: int):
    return Board(size)


def __next(size: int, board: Board):
    next = __next_permutation(board)
    return None if next.rows() == list(range(size)) else next


def __accept(size: int, board: Board):
    return board.is_valid()


def solve(size: int):
    for board in BruteForceSolver(__first, __next, __accept).solve(size):
        yield board
