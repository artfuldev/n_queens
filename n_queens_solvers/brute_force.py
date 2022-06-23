from models.board import Board
from solvers.brute_force import BruteForceSolver
from typing import Generator

def candidates(rows: list[int], index=0) -> Generator[Board, None, None]:
    length = len(rows)
    if index > length:
        return
    if index == length:
        yield Board(rows=rows)
    else:
        for i in range(index, length):
            rows[i], rows[index] = rows[index], rows[i]
            for candidate in candidates(rows, index + 1):
                yield candidate
            rows[index], rows[i] = rows[i], rows[index]

class Solver:
    def __init__(self, size: int):
        generator = candidates(list(range(size)))
        self.__solver = BruteForceSolver[Board, int](
            lambda size: next(generator),
            lambda size, board: next(generator, None),
            lambda size, board: board.is_valid()
        )
        self.__size = size

    def solve(self):
        return self.__solver.solve(self.__size)
