from random import choices, shuffle
from typing import Optional, Tuple
from algorithms.particle_swarm import Trip, Velocities, particle_swarm as algorithm
from domain.board import (
    Row,
    Size,
    Board,
    collisions,
    random_row_pair,
    random_row_pair_that_may_reduce_collisions,
    shuffled,
    swap_rows,
)
from solutions.from_optimizer import from_optimizer

Swap = Optional[Tuple[Row, Row]]


def __first(n: Size) -> list[Board]:
    return [shuffled(n) for _ in range(n)]


__velocity = random_row_pair_that_may_reduce_collisions


def __quality(n: Size, board: Board) -> float:
    return (pow(n, 2) - collisions(n, board)) * 100 / pow(n, 2)


def __terminate(n: Size, board: Board) -> bool:
    return __quality(n, board) == 100


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
        return random_row_pair(n) if optional_velocity is None else optional_velocity

    return swap


def __move(n: Size, board: Board, velocity: Swap) -> Board:
    return board if velocity is None else swap_rows(board, velocity)


def __output(_: Size, board: Board) -> Board:
    return board


particle_swarm = from_optimizer(
    algorithm(
        __first,
        __velocity,
        __quality,
        __terminate,
        __plan,
        __next(0.8, 0.5, 1.5),
        __move,
        __output,
    )
)
