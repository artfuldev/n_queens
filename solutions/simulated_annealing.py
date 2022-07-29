from math import exp, floor
from domain.board import (
    Board,
    Size,
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
from solutions.from_optimizer import from_optimizer

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


__steps = 10
__alpha = 0.97

anneal = from_optimizer(
    algorithm(
        __first,
        __budget(__steps),
        __neighbor,
        __temperature(__steps, __alpha),
        __energy,
        __terminate,
        __accept,
    )
)
