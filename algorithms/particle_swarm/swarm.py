from dataclasses import dataclass
from typing import Callable, List

from .particle import Particle, Position


@dataclass
class Swarm:
    particles: List[Particle]
    best: Position


def from_particles(
    quality: Callable[[Position], float]
) -> Callable[[List[Particle]], Swarm]:
    def create(particles: List[Particle]) -> Swarm:
        best = max(particles, key=lambda p: quality(p.position))
        return Swarm(particles, best.position)

    return create
