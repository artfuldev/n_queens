from dataclasses import dataclass
from random import uniform
from typing import Callable, List, NewType, TypeVar
from algorithms.solve import Solve

Problem = TypeVar("Problem")
Solution = TypeVar("Solution")
Position = NewType("Position", List[float])
Velocity = NewType("Velocity", List[float])


@dataclass
class Particle:
    position: Position
    velocity: Velocity
    best: Position


@dataclass
class Swarm:
    particles: List[Particle]
    best: Position


@dataclass(frozen=True)
class Range:
    low: float
    high: float


def __move(limits: list[Range], position: Position, velocity: Velocity) -> Position:
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


def __initialize(
    swarm_size: int, limits: List[Range], quality: Callable[[Position], float]
) -> Swarm:
    dimensions = list(range(len(limits)))
    swarm = Swarm([], Position(list(map(lambda r: uniform(r.low, r.high), limits))))
    for _ in range(swarm_size):
        position = Position([])
        velocity = Velocity([])
        for dimension in dimensions:
            low = limits[dimension].low
            high = limits[dimension].high
            position.append(uniform(low, high))
            abs_range = abs(high - low)
            velocity.append(uniform(-abs_range, abs_range))
        particle = Particle(position, velocity, position)
        swarm.particles.append(particle)
        if quality(position) > quality(swarm.best):
            swarm.best = position
    return swarm


def particle_swarm(
    size: Callable[[Problem], int],
    ranges: Callable[[Problem], List[Range]],
    quality: Callable[[Problem, Position], float],
    terminate: Callable[[Problem, Position], bool],
    velocity: Callable[[Problem, Particle, Position], Velocity],
    output: Callable[[Problem, Position], Solution],
) -> Solve[Problem, Solution]:
    def solve(problem: Problem):
        def solve(problem: Problem):
            _size = size(problem)
            _limits = ranges(problem)

            def _quality(position: Position) -> float:
                return quality(problem, position)

            swarm = __initialize(_size, _limits, _quality)
            while not terminate(problem, swarm.best):
                for i in range(_size):
                    swarm.particles[i].velocity = velocity(
                        problem,
                        swarm.particles[i],
                        swarm.best,
                    )
                    swarm.particles[i].position = __move(
                        _limits,
                        swarm.particles[i].position,
                        swarm.particles[i].velocity,
                    )
                    if _quality(swarm.particles[i].position) > _quality(
                        swarm.particles[i].best
                    ):
                        swarm.particles[i].best = swarm.particles[i].position
                        if _quality(swarm.particles[i].best) > _quality(swarm.best):
                            swarm.best = swarm.particles[i].best
            return output(problem, swarm.best)

        while True:
            yield solve(problem)

    return solve
