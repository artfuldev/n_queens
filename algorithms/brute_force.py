from typing import Callable, Generator, TypeVar

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")


def brute_force(
    first: Callable[[Problem], Candidate],
    next: Callable[[Problem, Candidate], Candidate | None],
    accept: Callable[[Problem, Candidate], bool],
) -> Callable[[Problem], Generator[Candidate, None, None]]:
    def solve(problem: Problem):
        candidate = first(problem)
        while candidate is not None:
            if accept(problem, candidate):
                yield candidate
            candidate = next(problem, candidate)

    return solve
