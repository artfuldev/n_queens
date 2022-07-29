from .transform import Problem, Solution
from .solve import Solve


def infinite(solve: Solve[Problem, Solution]) -> Solve[Problem, Solution]:
    def __solve(problem: Problem):
        while True:
            for solution in solve(problem):
                yield solution

    return __solve
