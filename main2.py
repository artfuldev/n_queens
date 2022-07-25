from copy import copy
from itertools import islice
from random import choice
from typing import Union, Literal
from math import exp
from algorithms.simulated_annealing import (
    Budget,
    Energy,
    RemainingBudget,
    NeighborEnergy,
    Probability,
    Temperature,
    anneal,
)

Bit = Union[Literal[1], Literal[0]]
Bits = list[Bit]
__bits: Bits = [0, 1]


def __bit() -> Bit:
    return choice(__bits)


def __flip(b: Bit) -> Bit:
    return 1 if b == 0 else 0


def __first(n: int) -> Bits:
    return [__bit() for _ in range(n)]


def __budget(n: int) -> Budget:
    return n * n


def __neighbor(n: int, bits: Bits) -> Bits:
    neighbor = copy(bits)
    i = choice(list(range(n)))
    neighbor[i] = __flip(neighbor[i])
    return neighbor


def __temperature(n: int, b: RemainingBudget) -> Temperature:
    return pow(0.97, ((1 - b) * n * n) - 1) * n * n


def __energy(n: int, bits: Bits) -> Energy:
    return n - sum(bits)


def __terminate(n: int, energy: Energy) -> bool:
    return energy == 0


def __probability(
    n: int, e: Energy, e_next: NeighborEnergy, t: Temperature
) -> Probability:
    return 1 if e_next < e else exp(-(e_next - e) / t)


def __key(n: int, bits: Bits) -> str:
    return "".join(map(str, bits))


def __accept(n: int, bits: Bits) -> bool:
    return __energy(n, bits) == 0


find_max = anneal(
    __first,
    __budget,
    __neighbor,
    __temperature,
    __energy,
    __terminate,
    __probability,
    __key,
    __accept,
)

for solution in islice(find_max(20), 1):
    print(solution)
