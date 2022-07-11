from copy import deepcopy
from functools import partial
from math import floor
from random import choice, choices, randint, random, shuffle
from typing import Generator, Literal, Set, TypeAlias, Union, Tuple
from domain.board import Board, Column, Row, Size, has_collision, place_queen, row_pairs
from algorithms.genetic import Individual, genetic as algorithm


def __column(n: Size) -> Column:
    """returns a random column"""
    return Column(randint(0, n - 1))


def __board(n: Size) -> Board:
    """returns a random board with shuffled rows"""
    rows = list(range(n))
    shuffle(rows)
    return Board(rows)


def __population(n: Size) -> list[Board]:
    """returns a random population of n boards"""
    return [__board(n) for _ in range(n)]


def __collisions(n: Size, board: Board) -> list[Tuple[Row, Row]]:
    """returns a list of colliding row pairs"""
    return list(filter(partial(has_collision, board), row_pairs(n)))


def __fitness(n: Size, board: Board) -> float:
    """returns the fitness of a board"""
    return (pow(n, 2) - len(__collisions(n, board))) * 100 / pow(n, 2)


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
    return Board(child)


def __swap(board: Board, x: Row, y: Row):
    """swaps two rows and ensures no collisions"""
    return place_queen(place_queen(board, x, board[y]), y, board[x])


def __flatten(row_pairs: list[Tuple[Row, Row]]) -> list[Row]:
    """returns a (flat) list of all rows in a list of row pairs"""
    rows = set()
    for x, y in row_pairs:
        rows.add(x)
        rows.add(y)
    return list(rows)

def __mutate(n: Size, board: Board) -> Board:
    """returns a new board with a collided row swapped according to the mutation rate"""
    mutation_probability = 1 / n
    chance = random()
    if chance >= mutation_probability:
        return board
    colliding_row_pairs = __collisions(n, board)
    if len(colliding_row_pairs) == 0:
        return board
    x, y = choice(colliding_row_pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, __flatten(colliding_row_pairs)))
    return board if not any(y_choices) else __swap(board, x, choice(y_choices))


def __terminate(n: Size, individual: Individual[Board], generation: int) -> bool:
    """returns True if the algorithm should terminate"""
    return generation == n * 1000 or individual.fitness == 100


_algorithm = algorithm(__population, __fitness, __crossover, __mutate, __terminate)

def hash(board: Board) -> str:
    """returns a hash of a board"""
    return "".join(map(str, board))

def genetic(n: Size) -> Generator[Board, None, None]:
    """returns a generator of boards using the genetic algorithm"""
    uniques: Set[Board] = set()
    for individual in _algorithm(n):
        candidate_hash = hash(individual.candidate)
        if individual.fitness >= 100 and candidate_hash not in uniques:
            uniques.add(candidate_hash)
            yield individual.candidate

