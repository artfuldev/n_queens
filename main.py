from timeit import default_timer
from domain.reporter import report
from solutions.brute_force import brute_force
from solutions.back_tracking import back_tracking
from itertools import islice

solvers = {"brute_force": brute_force, "back_tracking": back_tracking}


def find_solutions(size: int, count=1, until: int = None, report=report):
    if count <= 0:
        raise
    stop = size + 1 if until is None else until + 1
    for n in range(size, stop):
        for name, solve in solvers.items():
            started = default_timer()
            solutions = list(islice(solve(n), count))
            ended = default_timer()
            print(report(n, ended - started, name, solutions))


find_solutions(4, count=pow(2, 30), until=10)
