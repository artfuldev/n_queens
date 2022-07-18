from dataclasses import dataclass
from random import choices
from typing import (
    Callable,
    Generator,
    Generic,
    Tuple,
    TypeAlias,
    TypeVar,
    cast,
)

from algorithms.solve import Solve


Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")

C: TypeAlias = Candidate
P: TypeAlias = Problem
S: TypeAlias = Solution


@dataclass(frozen=True)
class Individual(Generic[Candidate]):
    candidate: Candidate
    fitness: float


def individual_candidate(individual: Individual[C]):
    return individual.candidate


def individual_fitness(individual: Individual[C]) -> float:
    return individual.fitness


def __select(_: P, population: list[Individual[C]]) -> Tuple[C, C]:
    return cast(
        Tuple[C, C],
        list(
            map(
                individual_candidate,
                choices(
                    population, weights=list(map(individual_fitness, population)), k=2
                ),
            )
        ),
    )


@dataclass(frozen=True)
class Result(Individual[Candidate]):
    generations: int


def __result(_: P, individual: Individual[C], generations: int) -> Result[C]:
    return Result(individual.candidate, individual.fitness, generations)


def genetic(
    population: Callable[[P], list[C]],
    fitness: Callable[[P, C], float],
    crossover: Callable[[P, C, C], C],
    mutate: Callable[[P, C], C],
    terminate: Callable[[P, Individual[C], int], bool],
    select: Callable[[P, list[Individual[C]]], Tuple[C, C]] = __select,
    output: Callable[[P, Individual[C], int], S] = __result,
) -> Solve[P, S]:
    def solve(problem: P) -> Generator[S, None, None]:
        def solve(problem: P, population: list[C], generation: int) -> S:
            population_count = len(population)
            gene_pool = list(
                map(lambda c: Individual(c, fitness(problem, c)), population)
            )
            while True:
                for individual in gene_pool:
                    if terminate(problem, individual, generation):
                        return output(problem, individual, generation)
                next_gene_pool = []
                for i in range(population_count):
                    parent_1, parent_2 = select(problem, gene_pool)
                    child = crossover(problem, parent_1, parent_2)
                    mutated = mutate(problem, child)
                    next_gene_pool.append(
                        Individual(mutated, fitness(problem, mutated))
                    )
                gene_pool = next_gene_pool
                generation += 1

        while True:
            yield solve(problem, population(problem), 1)

    return solve
