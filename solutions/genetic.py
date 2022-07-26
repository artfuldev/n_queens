from random import choice, random

from domain.board import (
    Board,
    Size,
    cache_key,
    collisions,
    from_list,
    random_row_pair_that_may_reduce_collisions,
    shuffled,
    swap_rows,
)
from algorithms.genetic import Individual, genetic as algorithm


def __populate(n: Size) -> list[Board]:
    """returns a random population of n boards"""
    return [shuffled(n) for _ in range(n)]


def __fitness(n: Size, board: Board) -> float:
    """returns the fitness of a board"""
    return (pow(n, 2) - collisions(n, board)) * 100 / pow(n, 2)


def __crossover(n: Size, x: Board, y: Board) -> Board:
    """Returns a new child board with a selection of rows from parents"""
    fills = list(range(n))
    child = from_list([-1 for _ in range(n)])
    for i in range(n):
        if x[i] == y[i]:
            child = child.set(i, x[i])
            fills.remove(x[i])
        else:
            child = child.set(i, -1)
    for i in range(n):
        if child[i] == -1:
            child = child.set(i, choice(fills))
            fills.remove(child[i])
    return child


def __mutate(n: Size, board: Board) -> Board:
    """returns a new board with a collided row swapped according to the mutation rate"""
    mutation_probability = 1 / n
    chance = random()
    if chance >= mutation_probability:
        return board
    pair = random_row_pair_that_may_reduce_collisions(n, board)
    return board if pair is None else swap_rows(board, pair)


def __terminate(n: Size, population: list[Individual[Board]], generation: int) -> bool:
    """returns True if the algorithm should terminate"""
    return generation == n * 1000 or any(
        filter(lambda f: f == 100, map(lambda i: i.fitness, population))
    )


def __valid(n: Size, board: Board) -> bool:
    return __fitness(n, board) == 100


def __output(n: Size, individual: Individual[Board]) -> Board:
    return individual.candidate


def __key(n: Size, board: Board) -> str:
    return cache_key(board)


genetic = algorithm(
    __populate,
    __fitness,
    __crossover,
    __mutate,
    __terminate,
    __output,
    __key,
    __valid,
)
