from functools import reduce
from itertools import repeat
from random import choice, choices, shuffle
from typing import Tuple, cast
from algorithms.particle_swarm import Trip, Components, particle_swarm as algorithm
from domain.board import Column, Row, Size, Board, cache_key, colliding_row_pairs, swap
from domain.list import flatten, unique


def __board(n: Size) -> Board:
    board = Board(list(map(Column, range(n))))
    shuffle(board)
    return board


def __first(n: Size) -> list[Board]:
    return [__board(n) for _ in range(n)]


def __velocity(n: Size, board: Board) -> list[Tuple[Row, Row]]:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return []
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    return [] if len(y_choices) == 0 else [(x, choice(y_choices))]


def __quality(n: Size, board: Board) -> float:
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


def __terminate(n: Size, board: Board) -> bool:
    return __quality(n, board) == 100


def __plan(n: Size, trip: Trip[Board]) -> list[Tuple[Row, Row]]:
    pass


def __next(inertia: float, cognitive_coefficient: float, social_coefficient: float):
    def next_velocity(
        n: Size, components: Components[list[Tuple[Row, Row]]]
    ) -> list[Tuple[Row, Row]]:
        population = components.inertial + components.cognitive + components.social
        weights = (
            list(repeat(inertia, len(components.inertial)))
            + list(repeat(cognitive_coefficient, len(components.cognitive)))
            + list(repeat(social_coefficient, len(components.social)))
        )
        return choices(population, weights, k=1)

    return next_velocity


def __swap(board: Board, pair: Tuple[Row, Row]) -> Board:
    x, y = pair
    return swap(board, x, y)


def __apply(n: Size, board: Board, row_pairs: list[Tuple[Row, Row]]):
    return reduce(__swap, row_pairs, board)


def __cache_key(_: Size, board: Board) -> str:
    return cache_key(board)


particle_swarm = algorithm(
    __first,
    __velocity,
    __quality,
    __terminate,
    __plan,
    __next(0.4, 1.5, 3.0),
    __apply,
    __cache_key,
)
