from typing import Callable, Generator, TypeVar

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")

def __identity(_: Problem, candidate: Candidate):
    return candidate

def brute_force(
    first: Callable[[Problem], Candidate | None],
    next: Callable[[Problem, Candidate], Candidate | None],
    accept: Callable[[Problem, Candidate], bool],
    output: Callable[[Problem, Candidate], Solution] = __identity
) -> Callable[[Problem], Generator[Solution, None, None]]:
    def solve(problem: Problem):
        candidate = first(problem)
        while candidate is not None:
            if accept(problem, candidate):
                yield output(problem, candidate)
            candidate = next(problem, candidate)

    return solve
