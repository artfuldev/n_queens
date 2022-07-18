from functools import partial
from typing import Callable, List, Tuple, TypeAlias, TypeVar
from algorithms.solve import Solve

Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")

Position: TypeAlias = Tuple[int, ...]
Magnitude: TypeAlias = float
Direction: TypeAlias = Tuple[int, ...]
Velocity: TypeAlias = Tuple[Magnitude, Direction]
Particle: TypeAlias = Tuple[Position, Velocity]
Swarm: TypeAlias = List[Particle]
State: TypeAlias = Tuple[Swarm, Position]
Step: TypeAlias = int

def particle_swarm(
    candidates: Callable[[Problem], List[Candidate]],
    velocity: Callable[[Problem, Step], Magnitude],
    down: Callable[[Problem, Candidate], Position],
    up: Callable[[Problem, Position], Candidate],
    quality: Callable[[Problem, Candidate], float],
    steps: Callable[[Problem], int],
) -> Solve[Problem, Solution]:
    def solve(problem: Problem):
        step = 0
        magnitude = velocity(problem, step)
        swarm_candidates = candidates(problem)
        global_best = down(problem, (max(swarm_candidates, key=lambda c: quality(problem, c))))
        swarm = []
        for candidate in swarm_candidates:
            position = down(problem, candidate)
            particle = [position, ]
            swarm.append(particle)
        pass
    
    return solve
