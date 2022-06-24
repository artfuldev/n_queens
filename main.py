from timeit import default_timer
from models.reporter import report
from solutions.brute_force import brute_force
from solutions.back_tracking import back_tracking
from itertools import islice

summary = "size {:3d}, {:3d} solution{}, {:0.3f}s, {}"


def find_solutions(size: int, count=1, until: int = None, report=report):
    stop = size + 1 if until is None else until + 1
    for n in range(size, stop):
        if count <= 0:
            raise
        started = default_timer()
        solutions = list(islice(back_tracking(n), count))
        ended = default_timer()
        print(report(n, ended - started, solutions))


find_solutions(4, count=100, until=9)
