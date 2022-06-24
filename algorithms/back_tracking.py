from typing import Callable, Generator, TypeVar

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


def back_tracking(
    root: Callable[[Problem], Candidate],
    reject: Callable[[Problem, Candidate], bool],
    accept: Callable[[Problem, Candidate], bool],
    output: Callable[[Problem, Candidate], Solution],
    first: Callable[[Problem, Candidate], Candidate],
    next: Callable[[Problem, Candidate], Candidate | None],
):

    def try_solve(
        problem: Problem, candidate: Candidate
    ) -> Generator[Solution, None, None]:
        if accept(problem, candidate):
            yield output(problem, candidate)
            return
        extension = first(problem, candidate)
        while extension is not None:
            if not reject(problem, extension):
                for solution in try_solve(problem, extension):
                    yield solution
            extension = next(problem, extension)

    def solve(problem: Problem):
        return try_solve(problem, root(problem))

    return solve
