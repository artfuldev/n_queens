from dataclasses import dataclass
from functools import partial
from typing import Callable, Generic, TypeVar

from .from_optimizer import from_optimizer
from .solve import Problem, Solve

Solution = TypeVar("Solution")
Position = TypeVar("Position")
Velocity = TypeVar("Velocity")


@dataclass
class Particle(Generic[Position, Velocity]):
    position: Position
    velocity: Velocity
    best: Position


def __particle(position: Position, velocity: Velocity) -> Particle[Position, Velocity]:
    return Particle(position, velocity, position)


def __always(problem: Problem, solution: Solution) -> bool:
    return True


def __position(problem: Problem, position: Position):
    return position


@dataclass(frozen=True)
class Components(Generic[Velocity]):
    inertial: Velocity
    cognitive: Velocity
    social: Velocity


@dataclass(frozen=True)
class Positions(Generic[Position]):
    current: Position
    best: Position


def particle_swarm(
    first: Callable[[Problem], list[Position]],
    velocity: Callable[[Problem, Position], Velocity],
    quality: Callable[[Problem, Position], float],
    terminate: Callable[[Problem, Position], bool],
    cognitive: Callable[[Problem, Positions[Position]], Velocity],
    social: Callable[[Problem, Positions[Position]], Velocity],
    next: Callable[[Problem, Components[Velocity]], Velocity],
    apply: Callable[[Problem, Position, Velocity], Position],
    key: Callable[[Problem, Solution], str],
    output: Callable[[Problem, Position], Solution] = __position,
    accept: Callable[[Problem, Solution], bool] = __always,
) -> Solve[Problem, Solution]:
    def optimize(problem: Problem) -> Solution:
        particles = list(
            map(lambda p: __particle(p, velocity(problem, p)), first(problem))
        )
        best = max(
            map(lambda particle: particle.best, particles),
            key=partial(quality, problem),
        )
        while not terminate(problem, best):
            for particle in particles:
                particle.velocity = next(
                    problem,
                    Components(
                        particle.velocity,
                        cognitive(problem, Positions(particle.position, particle.best)),
                        social(problem, Positions(particle.position, best)),
                    ),
                )
                particle.position = apply(problem, particle.position, particle.velocity)
                particle.best = max(
                    particle.position,
                    particle.best,
                    key=partial(quality, problem),
                )
                best = max(
                    map(lambda particle: particle.best, particles),
                    key=partial(quality, problem),
                )
        return output(problem, best)

    return from_optimizer(key, accept, optimize)
