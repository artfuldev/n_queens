from timeit import default_timer
from algorithms.solve import Solve
from domain.board import Board, Size
from domain.report import Report, stringify
from solutions.brute_force import brute_force
from solutions.back_tracking import back_tracking
from solutions.genetic import genetic
from solutions.particle_swarm import particle_swarm
from itertools import islice


__solvers: dict[str, Solve[Size, Board]] = {
    "brute_force": brute_force,
    "back_tracking": back_tracking,
    "genetic": genetic,
    "particle_swarm": particle_swarm,
}


def find_solutions(size: int, count=1, until: int = None):
    if count <= 0:
        raise
    stop = size + 1 if until is None else until + 1
    for i in range(size, stop):
        n = Size(i)
        n_count = count
        for algorithm, solve in __solvers.items():
            started = default_timer()
            solutions = list(islice(solve(n), n_count))
            n_count = len(solutions)
            ended = default_timer()
            yield Report(algorithm, n, solutions, ended - started)


for report in find_solutions(4, until=8):
    print(stringify(report))
