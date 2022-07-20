from math import floor, factorial
from random import random
from algorithms.particle_swarm import (
    Particle,
    Position,
    Range,
    Velocity,
    particle_swarm as algorithm,
)
from domain.board import Column, Size, Board, cache_key, colliding_row_pairs


def __nth_permutation(s: Size, n: int) -> list[int]:
    items = list(range(s))
    res: list[int] = []
    for x in range(s - 1, -1, -1):
        f = factorial(x)
        d = n // f
        n -= d * f
        res.append(items[d])
        del items[d]
    return res


def __size(n: Size) -> int:
    return n

def __ranges(n: Size) -> list[Range]:
    return [Range(0, factorial(n) - 0.000000001)]


def __board(s: Size, position: Position) -> Board:
    return Board(list(map(Column, __nth_permutation(s, floor(position[0])))))


def __quality(s: Size, position: Position) -> float:
    return (
        (pow(s, 2) - len(colliding_row_pairs(s, __board(s, position))))
        * 100
        / pow(s, 2)
    )


def __terminate(n: Size, position: Position) -> bool:
    return __quality(n, position) == 100


def __velocity(w: float, phi_p: float, phi_g: float):
    def velocity(_: Size, particle: Particle, g_best: Position) -> Velocity:
        x = particle.position
        v = particle.velocity
        p_best = particle.best
        r_p = random()
        r_g = random()
        next_v = []
        for d in range(len(v)):
            next_v.append(
                (w * v[d])
                + (phi_p * r_p * (p_best[d] - x[d]))
                + (phi_g * r_g * (g_best[d] - x[d]))
            )
        return Velocity(next_v)

    return velocity


def __cache_key(_: Size, board: Board) -> str:
    return cache_key(board)


particle_swarm = algorithm(
    __size,
    __ranges,
    __quality,
    __terminate,
    __velocity(0.6, 1.5, 3),
    __board,
    __cache_key,
)
