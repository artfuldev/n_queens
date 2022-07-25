from dataclasses import dataclass
from random import uniform
from typing import Generic, TypeVar, Callable, Any

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


@dataclass(frozen=True)
class State(Generic[System]):
    system: System
    energy: Energy


def __create_state(system: System, energy: Callable[[System], Energy]) -> State[System]:
    return State(system, energy(system))


def __always(problem: Any, system: Any):
    return True


def anneal(
    first: Callable[[Problem], System],
    budget: Callable[[Problem], Budget],
    neighbor: Callable[[Problem, System], System],
    temperature: Callable[[Problem, RemainingBudget], Temperature],
    energy: Callable[[Problem, System], Energy],
    terminate: Callable[[Problem, Energy], bool],
    probability: Callable[[Problem, Energy, NeighborEnergy, Temperature], Probability],
    key: Callable[[Problem, System], str],
    valid: Callable[[Problem, System], bool] = __always,
) -> Solve[Problem, System]:
    def optimize(problem: Problem) -> System:
        def __state(system: System) -> State[System]:
            return State(system, energy(problem, system))
        state = __state(first(problem))
        k_max = budget(problem)
        for k in range(k_max):
            current_temperature = temperature(problem, 1 - ((k + 1) / k_max))
            if terminate(problem, state.energy):
                return state.system
            state_next = __state(neighbor(problem, state.system))
            acceptance_probability = probability(
                problem, state.energy, state_next.energy, current_temperature
            )
            if acceptance_probability > uniform(0, 1):
                state = state_next
        return state.system

    return from_optimizer(key, valid, optimize)
