from typing import Callable

from .transform import Problem, Solution, Transform
from .solve import Solve


def valid(
    predicate: Callable[[Problem, Solution], bool]
) -> Transform[Problem, Solution]:
    def transform(solve: Solve[Problem, Solution]) -> Solve[Problem, Solution]:
        def __solve(problem: Problem):
            for solution in solve(problem):
                if predicate(problem, solution):
                    yield solution

        return __solve

    return transform
