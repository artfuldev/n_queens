from typing import Callable
from domain.board import Board

summary = "size: {:3d}, solutions: {:5d}, time: {:8.3f}s, method: {:20s}, last: {}"


def report(size: int, seconds: int, name: str, solutions: list[Board]) -> str:
    return summary.format(
        size,
        len(solutions),
        seconds,
        name.rjust(20),
        solutions[-1] if any(solutions) else None,
    )
