from typing import Callable, List, TypeVar

from ..from_optimizer import from_optimizer
from .particle import (
    Particle,
    Range,
    Position,
    Velocity,
    from_limits,
    move_within,
)
from .swarm import from_particles
from ..solve import Problem, Solve


Solution = TypeVar("Solution")


def __always(problem: Problem, solution: Solution) -> bool:
    return True


def particle_swarm(
    size: Callable[[Problem], int],
    ranges: Callable[[Problem], List[Range]],
    quality: Callable[[Problem, Position], float],
    terminate: Callable[[Problem, Position], bool],
    velocity: Callable[[Problem, Particle, Position], Velocity],
    output: Callable[[Problem, Position], Solution],
    key: Callable[[Problem, Solution], str],
    accept: Callable[[Problem, Solution], bool] = __always,
) -> Solve[Problem, Solution]:
    def optimize(problem: Problem) -> Solution:
        _size = size(problem)
        _limits = ranges(problem)
        _move = move_within(_limits)

        def _quality(position: Position) -> float:
            return quality(problem, position)

        particles = [from_limits(_limits) for _ in range(_size)]
        swarm = from_particles(_quality)(particles)
        while not terminate(problem, swarm.best):
            for i in range(_size):
                particle = swarm.particles[i]
                particle.velocity = velocity(problem, particle, swarm.best)
                particle.position = _move(particle.position, particle.velocity)
                if _quality(particle.position) > _quality(particle.best):
                    particle.best = particle.position
                    if _quality(particle.best) > _quality(swarm.best):
                        swarm.best = particle.best
        return output(problem, swarm.best)

    return from_optimizer(key, accept, optimize)
