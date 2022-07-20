from dataclasses import dataclass
from random import uniform
from typing import Callable, List, NewType

Position = NewType("Position", List[float])
Velocity = NewType("Velocity", List[float])


@dataclass
class Particle:
    position: Position
    velocity: Velocity
    best: Position


@dataclass(frozen=True)
class Range:
    low: float
    high: float


def from_limits(limits: List[Range]) -> Particle:
    dimensions = list(range(len(limits)))
    position = Position([])
    velocity = Velocity([])
    for dimension in dimensions:
        low = limits[dimension].low
        high = limits[dimension].high
        position.append(uniform(low, high))
        abs_range = abs(high - low)
        velocity.append(uniform(-abs_range, abs_range))
    return Particle(position, velocity, position)


def move_within(limits: list[Range]) -> Callable[[Position, Velocity], Position]:
    def move(position: Position, velocity: Velocity) -> Position:
        next_position = []
        for d in range(len(limits)):
            limit = limits[d]
            next_value = position[d] + velocity[d]
            while (next_value > limit.high) or (next_value < limit.low):
                if next_value > limit.high:
                    next_value = (2 * limit.high) - next_value
                if next_value < limit.low:
                    next_value = (2 * limit.low) - next_value
            next_position.append(next_value)
        return Position(next_position)

    return move
