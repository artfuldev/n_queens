from random import choice, random, shuffle
from typing import Tuple

from domain.board import (
    Board,
    Column,
    Row,
    Size,
    cache_key,
    colliding_row_pairs,
    place_queen,
)
from algorithms.genetic import Individual, genetic as algorithm


def __board(n: Size) -> Board:
    """returns a random board with shuffled rows"""
    rows = list(map(Column, range(n)))
    shuffle(rows)
    return Board(rows)


def __population(n: Size) -> list[Board]:
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
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return board
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, __flatten(pairs)))
    return board if not any(y_choices) else __swap(board, x, choice(y_choices))


def __terminate(n: Size, individual: Individual[Board], generation: int) -> bool:
    """returns True if the algorithm should terminate"""
    return generation == n * 1000 or individual.fitness == 100


def __accept(n: Size, board: Board) -> bool:
    return __fitness(n, board) == 100


def __cache_key(n: Size, board: Board) -> str:
    return cache_key(board)


genetic = algorithm(
    __population,
    __fitness,
    __crossover,
    __mutate,
    __terminate,
    __cache_key,
    __accept,
)
