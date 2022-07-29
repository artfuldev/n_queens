from typing import Callable

from .transform import Problem, Solution, Transform
from .solve import Solve


def distinct(key: Callable[[Problem, Solution], str]) -> Transform[Problem, Solution]:
    def transform(solve: Solve[Problem, Solution]):
        def __solve(problem: Problem):
            cached_keys: set[str] = set()
            for solution in solve(problem):
                solution_key = key(problem, solution)
                if solution_key not in cached_keys:
                    cached_keys.add(solution_key)
                    yield solution

        return __solve

    return transform
