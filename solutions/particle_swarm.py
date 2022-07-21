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


def __pair(n: Size) -> Tuple[Row, Row]:
    return cast(Tuple[Row, Row], choices(range(n), k=2))


def __velocity(n: Size, board: Board) -> Tuple[Row, Row]:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return __pair(n)
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    return __pair(n) if len(y_choices) == 0 else (x, choice(y_choices))


def __quality(n: Size, board: Board) -> float:
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


def __terminate(n: Size, board: Board) -> bool:
    return __quality(n, board) == 100


def __plan(n: Size, trip: Trip[Board]) -> Tuple[Row, Row]:
    return __velocity(n, trip.source)


def __next(inertia: float, cognitive_coefficient: float, social_coefficient: float):
    def next_velocity(
        n: Size, components: Components[Tuple[Row, Row]]
    ) -> Tuple[Row, Row]:
        return choices(
            (components.inertial, components.cognitive, components.social),
            (inertia, cognitive_coefficient, social_coefficient),
            k=1,
        )[0]

    return next_velocity


def __apply(n: Size, board: Board, row_pair: Tuple[Row, Row]):
    x, y = row_pair
    return swap(board, x, y)


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
