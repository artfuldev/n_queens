from dataclasses import dataclass
from random import choices
from typing import Callable, Generic, Tuple, TypeVar, cast, Any

from .from_optimizer import from_optimizer
from .solve import Solve


_C = TypeVar("_C")
_P = TypeVar("_P")
_S = TypeVar("_S")

_T = TypeVar("_T")


@dataclass(frozen=True)
class Individual(Generic[_T]):
    candidate: _T
    fitness: float
    generation: int


def __select(_: Any, population: list[Individual[_T]]) -> Tuple[_T, _T]:
    items = list(map(lambda i: i.candidate, population))
    weights = list(map(lambda i: i.fitness, population))
    selected = choices(items, weights, k=2)
    return cast(Tuple[_T, _T], selected)


def __always(problem: Any, solution: Any) -> bool:
    return True


def genetic(
    populate: Callable[[_P], list[_C]],
    fitness: Callable[[_P, _C], float],
    crossover: Callable[[_P, _C, _C], _C],
    mutate: Callable[[_P, _C], _C],
    terminate: Callable[[_P, list[Individual[_C]], int], bool],
    output: Callable[[_P, Individual[_C]], _S],
    key: Callable[[_P, _S], str],
    valid: Callable[[_P, _S], bool] = __always,
    select: Callable[[_P, list[Individual[_C]]], Tuple[_C, _C]] = __select,
) -> Solve[_P, _S]:
    def optimize(problem: _P) -> _S:
        population = populate(problem)
        generation = 1
        population_count = len(population)
        gene_pool = sorted(
            map(lambda c: Individual(c, fitness(problem, c), generation), population),
            key=lambda i: i.fitness,
            reverse=True,
        )
        while not terminate(problem, gene_pool, generation):
            generation += 1
            next_gene_pool: list[Individual[_C]] = []
            for _ in range(population_count):
                parent_1, parent_2 = select(problem, gene_pool)
                child = crossover(problem, parent_1, parent_2)
                mutated = mutate(problem, child)
                next_gene_pool.append(
                    Individual(mutated, fitness(problem, mutated), generation)
                )
            gene_pool = sorted(next_gene_pool, key=lambda i: i.fitness, reverse=True)
        return output(problem, gene_pool[0])

    return from_optimizer(key, valid, optimize)
