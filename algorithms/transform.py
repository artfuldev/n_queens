from typing import Protocol, TypeVar

from .solve import Solve

Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


class Transform(Protocol[Problem, Solution]):
    def __call__(self, solve: Solve[Problem, Solution]) -> Solve[Problem, Solution]:
        pass
