from random import uniform
from typing import TypeVar, Callable

from .optimize import Optimize

System = TypeVar("System")
Problem = TypeVar("Problem")
Budget = int
Energy = float
Temperature = float
RemainingBudget = float
CandidateEnergy = Energy
Probability = float


def anneal(
    first: Callable[[Problem], System],
    budget: Callable[[Problem], Budget],
    neighbor: Callable[[Problem, System], System],
    temperature: Callable[[Problem, RemainingBudget], Temperature],
    energy: Callable[[Problem, System], Energy],
    terminate: Callable[[Problem, System], bool],
    accept: Callable[[Problem, Energy, CandidateEnergy, Temperature], Probability],
) -> Optimize[Problem, System]:
    def optimize(problem: Problem) -> System:
        system = first(problem)
        steps = budget(problem)
        for step in range(steps):
            if terminate(problem, system):
                return system
            candidate = neighbor(problem, system)
            acceptance_probability = accept(
                problem,
                energy(problem, system),
                energy(problem, candidate),
                temperature(problem, 1 - ((step + 1) / steps)),
            )
            if acceptance_probability >= uniform(0, 1):
                system = candidate
        return system

    return optimize
