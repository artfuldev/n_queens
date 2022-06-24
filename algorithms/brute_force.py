from typing import Callable, Generator, TypeVar

C = TypeVar("C")
P = TypeVar("P")


def brute_force(
    first: Callable[[P], C],
    next: Callable[[P, C], C | None],
    accept: Callable[[P, C], bool],
) -> Callable[[P], Generator[C, None, None]]:
    def solve(problem: P):
        candidate = first(problem)
        while candidate is not None:
            if accept(problem, candidate):
                yield candidate
            candidate = next(problem, candidate)

    return solve
