from typing import Callable
from models.board import Board

Reporter = Callable[[int, int, list[Board]], str]

summary = "size {:3d}, {:3d} solution{}, {:0.3f}s, {:20s}, {}"


def report(size: int, seconds: int, name: str, solutions: list[Board]) -> str:
    solutions_count = len(solutions)
    if solutions_count != 0:
        return summary.format(
            size,
            solutions_count,
            "s" if solutions_count != 1 else "",
            seconds,
            name,
            solutions[-1],
        )
    else:
        return summary.format(
            size,
            0,
            "s",
            seconds,
            name,
            None,
        )
