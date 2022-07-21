from dataclasses import dataclass
from functools import partial
from typing import Callable, Generic, Iterable, TypeVar

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
class Velocities(Generic[Velocity]):
    inertial: Velocity
    cognitive: Velocity
    social: Velocity


@dataclass(frozen=True)
class Trip(Generic[Position]):
    source: Position
    destination: Position


def particle_swarm(
    first: Callable[[Problem], list[Position]],
    velocity: Callable[[Problem, Position], Velocity],
    quality: Callable[[Problem, Position], float],
    terminate: Callable[[Problem, Position], bool],
    plan: Callable[[Problem, Trip[Position]], Velocity],
    next: Callable[[Problem, Velocities[Velocity]], Velocity],
    apply: Callable[[Problem, Position, Velocity], Position],
    key: Callable[[Problem, Solution], str],
    output: Callable[[Problem, Position], Solution] = __position,
    accept: Callable[[Problem, Solution], bool] = __always,
) -> Solve[Problem, Solution]:
    def optimize(problem: Problem) -> Solution:
        def best(positions: Iterable[Position]):
            return max(positions, key=partial(quality, problem))

        particles = list(
            map(lambda p: __particle(p, velocity(problem, p)), first(problem))
        )
        global_best = best(map(lambda particle: particle.best, particles))
        while not terminate(problem, global_best):
            for particle in particles:
                particle.velocity = next(
                    problem,
                    Velocities(
                        particle.velocity,
                        plan(problem, Trip(particle.position, particle.best)),
                        plan(problem, Trip(particle.position, global_best)),
                    ),
                )
                particle.position = apply(problem, particle.position, particle.velocity)
                particle.best = best((particle.position, particle.best))
                global_best = best((particle.best, global_best))
        return output(problem, global_best)

    return from_optimizer(key, accept, optimize)
