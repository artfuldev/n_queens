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


def __budget(steps: int):
    def budget(n: Size) -> Budget:
        return n * n * steps

    return budget


def __neighbor(n: Size, board: Board) -> Board:
    pair = random_row_pair_that_may_reduce_collisions(n, board)
    return swap_rows(board, pair if pair is not None else random_row_pair(n))


def __temperature(steps: int, alpha: float):
    def temperature(n: Size, b: RemainingBudget) -> Temperature:
        step = floor(((1 - b) * __budget(steps)(n)) - 1) // steps
        return pow(alpha, step) * n

    return temperature


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


__steps = 10
__alpha = 0.97

anneal = algorithm(
    __first,
    __budget(__steps),
    __neighbor,
    __temperature(__steps, __alpha),
    __energy,
    __terminate,
    __accept,
    __key,
    __valid,
)
