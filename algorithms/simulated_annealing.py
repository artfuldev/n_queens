from random import choices
from typing import TypeVar, Callable, Any

from .solve import Solve
from .from_optimizer import from_optimizer

System = TypeVar("System")
Problem = TypeVar("Problem")
Budget = int
Energy = float
Temperature = float
RemainingBudget = float
NeighborEnergy = Energy
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
    accept: Callable[[Problem, Energy, NeighborEnergy, Temperature], Probability],
    key: Callable[[Problem, System], str],
    valid: Callable[[Problem, System], bool] = __always,
) -> Solve[Problem, System]:
    def optimize(problem: Problem) -> System:
        s = first(problem)
        k_max = budget(problem)
        for k in range(k_max):
            if terminate(problem, s):
                return s
            s_new = neighbor(problem, s)
            p = accept(
                problem,
                energy(problem, s),
                energy(problem, s_new),
                temperature(problem, 1 - ((k + 1) / k_max)),
            )
            s = choices([s, s_new], [1 - p, p], k=1)[0]
        return s

    return from_optimizer(key, valid, optimize)
