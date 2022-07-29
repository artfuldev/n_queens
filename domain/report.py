from dataclasses import dataclass

from numpy import array, percentile
from .board import Board, Size, cache_key

summary = "size: {:3d}, solutions: {:5d}, p99: {:7.3f}s, method: {:15s}, last: {}"


@dataclass(frozen=True)
class TimedSolution:
    seconds: float
    board: Board


@dataclass(frozen=True)
class Report:
    algorithm: str
    size: Size
    solutions: list[TimedSolution]


def stringify(report: Report) -> str:
    return summary.format(
        report.size,
        len(report.solutions),
        percentile(list(map(lambda s: s.seconds, report.solutions)), 99),
        report.algorithm.rjust(20),
        cache_key(report.solutions[-1].board) if any(report.solutions) else None,
    )
