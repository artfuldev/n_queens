from dataclasses import dataclass
from typing import Callable, Generator, Generic, Tuple, TypeVar


Candidate = TypeVar("Candidate")
Problem = TypeVar("Problem")
Solution = TypeVar("Solution")


@dataclass
class Individual(Generic[Candidate]):
    candidate: Candidate
    fitness: float


def genetic(
    population: Callable[[Problem], list[Candidate]],
    fitness: Callable[[Problem, Candidate], float],
    selection: Callable[
        [Problem, list[Individual[Candidate]]], Tuple[Candidate, Candidate]
    ],
    crossover: Callable[[Candidate, Candidate], Candidate],
    mutate: Callable[[Candidate], Candidate],
    accept: Callable[[Problem, Candidate], bool],
    output: Callable[
        [Problem, Candidate], Solution
    ] = lambda problem, candidate: candidate,
) -> Callable[[Problem], Solution]:
    def solve(problem: Problem):
        def solve(
            problem: Problem, population: list[Candidate]
        ) -> Generator[Solution, None, None]:
            population_count = len(population)
            gene_pool = list(
                map(lambda c: Individual(c, fitness(problem, c)), population)
            )
            while True:
                for individual in gene_pool:
                    if accept(problem, individual.candidate):
                        yield output(problem, individual.candidate)
                        return
                next_gene_pool = []
                for i in range(population_count):
                    parent_1, parent_2 = selection(problem, gene_pool)
                    child = crossover(parent_1, parent_2)
                    mutated = mutate(child)
                    next_gene_pool.append(
                        Individual(mutated, fitness(problem, mutated))
                    )
                gene_pool = next_gene_pool

        return solve(problem, population(problem))

    return solve
