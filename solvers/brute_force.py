from models.board import Board
from typing import Callable, Generator, Generic, TypeVar

C = TypeVar("C")
P = TypeVar("P")

class BruteForceSolver(Generic[C, P]):
    def __init__(
        self,
        root: Callable[[P], C],
        next: Callable[[P, C], C | None],
        accept: Callable[[P, C], bool]
    ):
        self.__root = root
        self.__next = next
        self.__accept = accept
    
    def __brute_force(self, problem: P, candidate: C):
        while candidate is not None:
            if self.__accept(problem, candidate):
                yield candidate
            candidate = self.__next(problem, candidate)

    def solve(self, problem: P):
        return self.__brute_force(problem, self.__root(problem))
