from typing import Callable, Generator, TypeVar, Optional

from .solve import Solve

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


def back_tracking(
    root: Callable[[Problem], Optional[Candidate]],
    reject: Callable[[Problem, Candidate], bool],
    accept: Callable[[Problem, Candidate], bool],
    first: Callable[[Problem, Candidate], Optional[Candidate]],
    next: Callable[[Problem, Candidate], Optional[Candidate]],
    output: Callable[[Problem, Candidate], Solution],
) -> Solve[Problem, Solution]:
    def extend(
        problem: Problem, candidate: Candidate
    ) -> Generator[Solution, None, None]:
        if reject(problem, candidate):
            return
        if accept(problem, candidate):
            yield output(problem, candidate)
            return
        extension = first(problem, candidate)
        while extension is not None:
            for solution in extend(problem, extension):
                yield solution
            extension = next(problem, extension)

    def solve(problem: Problem):
        candidate = root(problem)
        if candidate is not None:
            for solution in extend(problem, candidate):
                yield solution

    return solve
