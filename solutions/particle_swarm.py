from functools import reduce
from random import choice, choices, randint, shuffle
from typing import Set, Tuple, cast
from algorithms.particle_swarm import Trip, Components, particle_swarm as algorithm
from domain.board import (
    Column,
    Row,
    Size,
    Board,
    cache_key,
    colliding_row_pairs,
    swap,
)
from domain.list import flatten, unique


def __board(n: Size) -> Board:
    board = Board(list(map(Column, range(n))))
    shuffle(board)
    return board


def __first(n: Size) -> list[Board]:
    return [__board(n) for _ in range(n)]


def __velocity(n: Size, board: Board) -> Tuple[Row, Row] | None:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return None
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    return None if len(y_choices) == 0 else (x, choice(y_choices))


def __quality(n: Size, board: Board) -> float:
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


def __terminate(n: Size, board: Board) -> bool:
    return __quality(n, board) == 100


def __distance(n: Size, a: Board, b: Board) -> int:
    return reduce(lambda d, i: d + abs(a[i] - b[i]), range(n), 0)


def __pair(n: Size) -> Tuple[Row, Row]:
    x = randint(0, n - 1)
    y = randint(0, n - 1)
    while x == y:
        y = randint(0, n - 1)
    return (Row(x), Row(y))


def __plan(n: Size, trip: Trip[Board]) -> Tuple[Row, Row] | None:
    def distance(board: Board):
        return __distance(n, board, trip.destination)

    _distance = distance(trip.source)
    if _distance == 0:
        return None
    seen: Set[Tuple[int, int]] = set()
    velocity = __velocity(n, trip.source)
    if velocity is not None:
        seen.add(velocity)
    x, y = __pair(n) if velocity is None else velocity
    next_distance = distance(swap(trip.source, x, y))
    while next_distance > _distance:
        velocity = __velocity(n, trip.source)
        x, y = __pair(n) if velocity is None or velocity in seen else velocity
        if velocity is not None:
            seen.add(velocity)
        next_distance = distance(swap(trip.source, x, y))
    return x, y


def __next(inertia: float, cognitive_coefficient: float, social_coefficient: float):
    def next_velocity(
        n: Size, components: Components[Tuple[Row, Row] | None]
    ) -> Tuple[Row, Row] | None:
        next_v = choices(
            (components.inertial, components.cognitive, components.social),
            (inertia, cognitive_coefficient, social_coefficient),
            k=1,
        )[0]
        return __pair(n) if next_v is None else next_v

    return next_velocity


def __apply(n: Size, board: Board, row_pair: Tuple[Row, Row] | None):
    if row_pair is None:
        return board
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
