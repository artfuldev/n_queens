from dataclasses import dataclass
from .board import Board, Size, cache_key

summary = "size: {:3d}, solutions: {:5d}, time: {:7.3f}s, method: {:15s}, last: {}"


@dataclass
class Report:
    algorithm: str
    size: Size
    solutions: list[Board]
    seconds: float


def stringify(report: Report) -> str:
    return summary.format(
        report.size,
        len(report.solutions),
        report.seconds,
        report.algorithm.rjust(20),
        cache_key(report.solutions[-1]) if any(report.solutions) else None,
    )
