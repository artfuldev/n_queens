from timeit import default_timer
from algorithms.solve import Solve
from domain.board import Board, Size
from domain.problem import Problem
from domain.report import Report, stringify
from solutions.brute_force import brute_force
from solutions.back_tracking import back_tracking
from solutions.genetic import genetic
from solutions.particle_swarm import particle_swarm
from solutions.simulated_annealing import anneal
from itertools import islice


__solvers: dict[str, Solve[Size, Board]] = {
    "brute_force": brute_force,
    "back_tracking": back_tracking,
    "genetic": genetic,
    "particle_swarm": particle_swarm,
    "simulated_annealing": anneal,
}


def solve(problem: Problem):
    started = default_timer()
    generator = __solvers[problem.algorithm](problem.size)
    solutions = list(islice(generator, problem.count))
    ended = default_timer()
    return Report(problem.algorithm, problem.size, solutions, ended - started)


def find_solutions(algorithms: list[str], size: int, count=1, until: int | None = None):
    if count <= 0:
        raise
    stop = size + 1 if until is None else until + 1
    for i in range(size, stop):
        n = Size(i)
        n_count = count
        for algorithm in algorithms:
            report = solve(Problem(Size(n), algorithm, n_count))
            n_count = len(report.solutions)
            yield report


__algorithms = [
    # "brute_force",
    "back_tracking",
    "genetic",
    "particle_swarm",
    "simulated_annealing",
]


for report in find_solutions(__algorithms, 4, until=200):
    print(stringify(report))
