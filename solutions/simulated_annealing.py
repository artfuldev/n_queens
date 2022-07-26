from math import exp, floor
from domain.board import (
    Board,
    Size,
    cache_key,
    collisions,
    random_row_pair,
    random_row_pair_that_may_reduce_collisions,
    shuffled,
    swap_rows,
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

__first = shuffled


def __budget(n: Size) -> Budget:
    return n * n * 10


def __neighbor(n: Size, board: Board) -> Board:
    pair = random_row_pair_that_may_reduce_collisions(n, board)
    return swap_rows(board, pair if pair is not None else random_row_pair(n))


def __temperature(n: Size, b: RemainingBudget) -> Temperature:
    step = floor(((1 - b) * __budget(n)) - 1) // 10
    return pow(0.97, step) * n


__energy = collisions


def __terminate(n: Size, board: Board) -> bool:
    return __energy(n, board) == 0


def __accept(
    n: Size, e: Energy, e_dash: CandidateEnergy, t: Temperature
) -> Probability:
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
