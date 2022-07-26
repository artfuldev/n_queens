from random import uniform
from typing import TypeVar, Callable, Any

from .solve import Solve
from .from_optimizer import from_optimizer

System = TypeVar("System")
Problem = TypeVar("Problem")
Budget = int
Energy = float
Temperature = float
RemainingBudget = float
CandidateEnergy = Energy
Probability = float


def __always(problem: Any, system: Any):
    return True


def anneal(
    first: Callable[[Problem], System],
    budget: Callable[[Problem], Budget],
    neighbor: Callable[[Problem, System], System],
    temperature: Callable[[Problem, RemainingBudget], Temperature],
    energy: Callable[[Problem, System], Energy],
    terminate: Callable[[Problem, System], bool],
    accept: Callable[[Problem, Energy, CandidateEnergy, Temperature], Probability],
    key: Callable[[Problem, System], str],
    valid: Callable[[Problem, System], bool] = __always,
) -> Solve[Problem, System]:
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

    return from_optimizer(key, valid, optimize)
