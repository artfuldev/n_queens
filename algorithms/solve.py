from typing import Generator, Protocol, TypeVar

Problem = TypeVar("Problem", contravariant=True)
Solution = TypeVar("Solution", covariant=True)

class Solve(Protocol[Problem, Solution]):
    def __call__(self, problem: Problem) -> Generator[Solution, None, None]:
        pass
