from timeit import default_timer
from models.reporter import report
from n_queens_solvers.brute_force import solve
from itertools import islice

summary = "size {:3d}, {:3d} solution{}, {:0.3f}s, {}"


def find_solutions(size: int, count=1, until: int = None, report=report):
    stop = size + 1 if until is None else until + 1
    for n in range(size, stop):
        if count <= 0:
            raise
        started = default_timer()
        solutions = list(islice(solve(n), count))
        ended = default_timer()
        print(report(size, ended - started, solutions))


find_solutions(4, until=9)
