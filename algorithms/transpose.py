from typing import Callable, Generator

from algorithms.solve import Solve
from algorithms.transform import Problem, Solution, Transform


def transpose(
    transpositions: Callable[[Solution], Generator[Solution, None, None]]
) -> Transform[Problem, Solution]:
    def transform(solve: Solve[Problem, Solution]) -> Solve[Problem, Solution]:
        def __solve(problem: Problem):
            for solution in solve(problem):
                for transposition in transpositions(solution):
                    yield transposition

        return __solve

    return transform
