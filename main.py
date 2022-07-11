from timeit import default_timer
from typing import Generator, Callable
from domain.board import Board, Size
from domain.reporter import report
from solutions.brute_force import brute_force
from solutions.back_tracking import back_tracking
from solutions.genetic import genetic
from itertools import islice


solvers: dict[str, Callable[[Size], Generator[Board, None, None]]] = {
    "brute_force": brute_force,
    "back_tracking": back_tracking,
    "genetic": genetic,
}


def find_solutions(size: int, count=1, until: int = None, report=report):
    """returns a generator of solutions for a given size of board"""
    if count <= 0:
        raise
    stop = size + 1 if until is None else until + 1
    for n in range(size, stop):
        n_count = count
        for name, solve in solvers.items():
            started = default_timer()
            solutions = list(islice(solve(Size(n)), n_count))
            n_count = len(solutions)
            ended = default_timer()
            print(report(n, ended - started, name, solutions))


find_solutions(4, count=pow(2, 30), until=10)
