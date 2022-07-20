from typing import Callable

from .solve import Problem, Solution, Solve


def from_optimizer(
    key: Callable[[Problem, Solution], str],
    accept: Callable[[Problem, Solution], bool],
    optimize: Callable[[Problem], Solution],
) -> Solve[Problem, Solution]:
    def solve(problem: Problem):
        cached_keys: set[str] = set()
        while True:
            solution = optimize(problem)
            if not accept(problem, solution):
                continue
            solution_key = key(problem, solution)
            if solution_key not in cached_keys:
                cached_keys.add(solution_key)
                yield solution

    return solve
