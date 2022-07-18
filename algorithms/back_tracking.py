from typing import Callable, Generator, TypeVar

from algorithms.solve import Solve

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


def __identity(_: Problem, candidate: Candidate):
    return candidate

def back_tracking(
    root: Callable[[Problem], Candidate | None],
    reject: Callable[[Problem, Candidate], bool],
    accept: Callable[[Problem, Candidate], bool],
    first: Callable[[Problem, Candidate], Candidate | None],
    next: Callable[[Problem, Candidate], Candidate | None],
    output: Callable[[Problem, Candidate], Solution] = __identity,
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
