from .optimize import Problem, Solution, Optimize
from .solve import Solve


def from_optimizer(optimize: Optimize[Problem, Solution]) -> Solve[Problem, Solution]:
    def solve(problem: Problem):
        yield optimize(problem)

    return solve
