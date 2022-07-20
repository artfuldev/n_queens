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
    generation: int


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


def __candidate(_: P, individual: Individual[C]) -> C:
    return individual.candidate


def __always(_: P, s: Solution) -> bool:
    return True


def genetic(
    population: Callable[[P], list[C]],
    fitness: Callable[[P, C], float],
    crossover: Callable[[P, C, C], C],
    mutate: Callable[[P, C], C],
    terminate: Callable[[P, Individual[C], int], bool],
    key: Callable[[P, S], str],
    select: Callable[[P, list[Individual[C]]], Tuple[C, C]] = __select,
    output: Callable[[P, Individual[C]], S] = __candidate,
    accept: Callable[[P, S], bool] = __always,
) -> Solve[P, S]:
    def solve(problem: P) -> Generator[S, None, None]:
        def solve_one(problem: P, population: list[C], generation: int) -> S:
            population_count = len(population)
            gene_pool = list(
                map(lambda c: Individual(c, fitness(problem, c), generation), population)
            )
            while True:
                for individual in gene_pool:
                    if terminate(problem, individual, generation):
                        return output(problem, individual)
                next_gene_pool = []
                generation += 1
                for _ in range(population_count):
                    parent_1, parent_2 = select(problem, gene_pool)
                    child = crossover(problem, parent_1, parent_2)
                    mutated = mutate(problem, child)
                    next_gene_pool.append(
                        Individual(mutated, fitness(problem, mutated), generation)
                    )
                gene_pool = next_gene_pool

        cached_keys: set[str] = set()
        while True:
            solution = solve_one(problem, population(problem), 1)
            if not accept(problem, solution):
                continue
            solution_key = key(problem, solution)
            if solution_key not in cached_keys:
                cached_keys.add(solution_key)
                yield solution

    return solve
