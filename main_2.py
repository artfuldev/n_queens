from functools import reduce
from itertools import islice
from random import random
from algorithms.particle_swarm import (
    Particle,
    Position,
    Range,
    Velocity,
    particle_swarm,
)


def __size(problem: int) -> int:
    return problem


def __ranges(problem: int) -> list[Range]:
    return [Range(0, 1) for _ in range(problem)]


def __quality(_: int, position: Position) -> float:
    return reduce(lambda x, y: x + 1 if y > 0.5 else x, position, 0.0)


class __Terminate:
    def __init__(self, steps: int):
        self.steps = 0
        self.limit = steps

    def __call__(self, problem: int, position: Position) -> bool:
        self.steps += 1
        terminate = (
            self.steps >= self.limit
            or reduce(lambda x, y: x + 1 if y > 0.5 else x, position, 0) == problem
        )
        if terminate:
            print(self.steps)
            self.steps = 0
        return terminate


def __velocity(w: float, phi_p: float, phi_g: float):
    def velocity(_: int, particle: Particle, g_best: Position) -> Velocity:
        x = particle.position
        v = particle.velocity
        p_best = particle.best
        r_p = random()
        r_g = random()
        next_v = []
        for i in range(len(v)):
            next_v.append(
                (w * v[i])
                + (phi_p * r_p * (p_best[i] - x[i]))
                + (phi_g * r_g * (g_best[i] - x[i]))
            )
        return Velocity(next_v)

    return velocity


def __output(_: int, position: Position) -> list[float]:
    return [1 if position[i] > 0.5 else 0 for i in range(len(position))]


find_max = particle_swarm(
    __size, __ranges, __quality, __Terminate(200), __velocity(0.6, 1.5, 3), __output
)

for solution in islice(find_max(20), 5):
    print(solution, sum(solution))
