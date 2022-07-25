from random import choice, randint
from typing import Tuple, cast
from math import exp
from domain.board import (
    Board,
    Row,
    Size,
    cache_key,
    colliding_row_pairs,
    shuffled,
    swap,
)
from algorithms.simulated_annealing import (
    Budget,
    Energy,
    RemainingBudget,
    CandidateEnergy,
    Probability,
    Temperature,
    anneal as algorithm,
)
from domain.list import flatten, unique

__first = shuffled


def __budget(n: Size) -> Budget:
    return n * n


def __pair(n: Size) -> Tuple[Row, Row]:
    x = randint(0, n - 1)
    y = randint(0, n - 1)
    while x == y:
        y = randint(0, n - 1)
    return (Row(x), Row(y))


def __swap(board: Board, row_pair: Tuple[Row, Row]) -> Board:
    x, y = row_pair
    return swap(board, x, y)


def __neighbor(n: Size, board: Board) -> Board:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return __swap(board, __pair(n))
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    row_pair = __pair(n) if len(y_choices) == 0 else (x, choice(y_choices))
    return __swap(board, row_pair)


def __temperature(n: Size, b: RemainingBudget) -> Temperature:
    return pow(0.97, ((1 - b) * n * n) - 1) * n


def __energy(n: Size, board: Board) -> Energy:
    return len(colliding_row_pairs(n, board))


def __terminate(n: Size, board: Board) -> bool:
    return __energy(n, board) == 0


def __accept(n: Size, e: Energy, e_dash: CandidateEnergy, t: Temperature) -> Probability:
    return 1 if e_dash < e else exp(-(e_dash - e) / t)


def __key(n: Size, board: Board) -> str:
    return cache_key(board)


def __valid(n: Size, board: Board) -> bool:
    return __energy(n, board) == 0


anneal = algorithm(
    __first,
    __budget,
    __neighbor,
    __temperature,
    __energy,
    __terminate,
    __accept,
    __key,
    __valid,
)
