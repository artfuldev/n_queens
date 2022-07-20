from dataclasses import dataclass
from .board import Size


@dataclass
class Problem:
    size: Size
    algorithm: str
    count: int
