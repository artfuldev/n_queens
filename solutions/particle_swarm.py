from random import choice, choices, randint, shuffle
from typing import Optional, Tuple, cast
from algorithms.particle_swarm import Trip, Velocities, particle_swarm as algorithm
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

Swap = Optional[Tuple[Row, Row]]


def __board(n: Size) -> Board:
    board = Board(list(map(Column, range(n))))
    shuffle(board)
    return board


def __first(n: Size) -> list[Board]:
    return [__board(n) for _ in range(n)]


def __velocity(n: Size, board: Board) -> Swap:
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


def __pair(n: Size) -> Swap:
    x = randint(0, n - 1)
    y = randint(0, n - 1)
    while x == y:
        y = randint(0, n - 1)
    return (Row(x), Row(y))


def __plan(n: Size, trip: Trip[Board]) -> Swap:
    if trip.source == trip.destination:
        return None
    reverse_index: dict[int, int] = {}
    for i in range(n):
        reverse_index[trip.destination[i]] = i
    candidates = list(range(n))
    shuffle(candidates)
    for i in candidates:
        x = Row(i)
        y = Row(reverse_index[trip.source[i]])
        if x != y:
            return (x, y)
    return None


def __next(inertia: float, cognitive_coefficient: float, social_coefficient: float):
    def swap(n: Size, velocities: Velocities[Swap]) -> Swap:
        optional_velocity = choices(
            (velocities.inertial, velocities.cognitive, velocities.social),
            (inertia, cognitive_coefficient, social_coefficient),
            k=1,
        )[0]
        return __pair(n) if optional_velocity is None else optional_velocity

    return swap


def __move(n: Size, board: Board, velocity: Swap) -> Board:
    if velocity is None:
        return board
    x, y = velocity
    return swap(board, x, y)


def __output(_: Size, board: Board) -> Board:
    return board


def __key(_: Size, board: Board) -> str:
    return cache_key(board)


particle_swarm = algorithm(
    __first,
    __velocity,
    __quality,
    __terminate,
    __plan,
    __next(0.8, 0.5, 1.5),
    __move,
    __output,
    __key,
)
