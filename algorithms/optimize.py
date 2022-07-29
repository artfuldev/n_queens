from typing import Protocol, TypeVar

Problem = TypeVar("Problem", contravariant=True)
Solution = TypeVar("Solution", covariant=True)


class Optimize(Protocol[Problem, Solution]):
    def __call__(self, problem: Problem) -> Solution:
        pass
