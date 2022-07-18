from typing import Callable, TypeVar
from algorithms.solve import Solve

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


def __identity(_: Problem, candidate: Candidate):
    return candidate


def brute_force(
    first: Callable[[Problem], Candidate | None],
    next: Callable[[Problem, Candidate], Candidate | None],
    accept: Callable[[Problem, Candidate], bool],
    output: Callable[[Problem, Candidate], Solution] = __identity,
) -> Solve[Problem, Solution]:
    def solve(problem: Problem):
        candidate = first(problem)
        while candidate is not None:
            if accept(problem, candidate):
                yield output(problem, candidate)
            candidate = next(problem, candidate)

    return solve
