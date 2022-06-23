from models.board import Board
from typing import Callable, Generator, Generic, TypeVar

T = TypeVar("T")


class BruteForceSolver(Generic[T]):
    def __init__(
        self, generator: Generator[T, None, None], accept: Callable[[T], bool]
    ):
        self.generator = generator
        self.accept = accept

    def solve(self) -> Generator[T, None, None]:
        for candidate in self.generator:
            if self.accept(candidate):
                yield candidate
