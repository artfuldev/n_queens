from random import choice, random, shuffle
from typing import Tuple, cast

from domain.board import (
    Board,
    Column,
    Row,
    Size,
    cache_key,
    colliding_row_pairs,
    place_queen,
    swap,
)
from algorithms.solve import Solve
from algorithms.genetic import Individual, genetic as algorithm, individual_fitness
from domain.list import flatten, unique


def __board(n: Size) -> Board:
    """returns a random board with shuffled rows"""
    rows = list(map(Column, range(n)))
    shuffle(rows)
    return Board(rows)


def __populate(n: Size) -> list[Board]:
    """returns a random population of n boards"""
    return [__board(n) for _ in range(n)]


def __fitness(n: Size, board: Board) -> float:
    """returns the fitness of a board"""
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


def __crossover(n: Size, x: Board, y: Board) -> Board:
    """Returns a new child board with a selection of rows from parents"""
    fills = list(range(n))
    child = [-1 for _ in range(n)]
    for i in range(n):
        if x[i] == y[i]:
            child[i] = x[i]
            fills.remove(x[i])
    for i in range(n):
        if child[i] == -1:
            child[i] = choice(fills)
            fills.remove(child[i])
    return Board(list(map(Column, child)))


def __mutate(n: Size, board: Board) -> Board:
    """returns a new board with a collided row swapped according to the mutation rate"""
    mutation_probability = 1 / n
    chance = random()
    if chance >= mutation_probability:
        return board
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return board
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    return board if not any(y_choices) else swap(board, x, choice(y_choices))


def __terminate(n: Size, population: list[Individual[Board]], generation: int) -> bool:
    """returns True if the algorithm should terminate"""
    return generation == n * 1000 or any(
        filter(lambda f: f == 100, map(individual_fitness, population))
    )


def __accept(n: Size, board: Board) -> bool:
    return __fitness(n, board) == 100


def __output(n: Size, individual: Individual[Board]) -> Board:
    return individual.candidate


def __cache_key(n: Size, board: Board) -> str:
    return cache_key(board)


genetic = algorithm(
    __populate,
    __fitness,
    __crossover,
    __mutate,
    __terminate,
    __output,
    __cache_key,
    __accept,
)
