from typing import Callable, Generator, TypeVar

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
):
    def try_solve(
        problem: Problem, candidate: Candidate
    ) -> Generator[Solution, None, None]:
        if reject(problem, candidate):
            return
        if accept(problem, candidate):
            yield output(problem, candidate)
            return
        extension = first(problem, candidate)
        while extension is not None:
            for solution in try_solve(problem, extension):
                yield solution
            extension = next(problem, extension)

    def solve(problem: Problem):
        candidate = root(problem)
        return None if candidate is None else try_solve(problem, candidate)

    return solve
