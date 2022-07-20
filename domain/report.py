from dataclasses import dataclass
from .board import Board, Size

summary = "size: {:3d}, solutions: {:5d}, time: {:6.3f}s, method: {:15s}, last: {}"


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
        report.algorithm.rjust(15),
        report.solutions[-1] if any(report.solutions) else None,
    )
