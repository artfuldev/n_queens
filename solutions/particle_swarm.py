from math import floor
from random import random
from algorithms.particle_swarm import (
    Particle,
    Position,
    Range,
    Velocity,
    particle_swarm as algorithm,
)
from domain.board import Column, Size, Board, cache_key, colliding_row_pairs


def __size(n: Size) -> int:
    return n


def __ranges(n: Size) -> list[Range]:
    return [Range(0, n - 0.000000001) for _ in range(n)]


def __quality(n: Size, position: Position) -> float:
    board = Board(list(map(Column, map(floor, position))))
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


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


def __output(_: Size, position: Position) -> Board:
    return Board(list(map(Column, map(floor, position))))

def __cache_key(_: Size, board: Board) -> str:
    return cache_key(board)

particle_swarm = algorithm(
    __size,
    __ranges,
    __quality,
    __terminate,
    __velocity(0.6, 1.5, 3),
    __output,
    __cache_key
)
