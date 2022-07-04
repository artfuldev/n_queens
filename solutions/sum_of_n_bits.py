from copy import deepcopy
from math import floor
from random import choice, randint, random
from typing import Literal, TypeAlias, Union

from algorithms.genetic import Individual, genetic


Bit: TypeAlias = Union[Literal[1], Literal[0]]
Bits: TypeAlias = list[Bit]
bit_choices: Bits = [1, 0]


def __bit() -> Bit:
    return choice(bit_choices)


def __flip(b: Bit) -> Bit:
    return 1 if b == 0 else 0


def __bits(n: int) -> Bits:
    return [__bit() for _ in range(n)]


def __population(n: int) -> list[Bits]:
    return [__bits(n) for _ in range(n)]


def __fitness(_: int, bits: Bits) -> float:
    return sum(bits)


def __crossover(n: int, x: Bits, y: Bits) -> Bits:
    return [x[i] if x[i] == y[i] else __bit() for i in range(n)]


def __mutate(n: int, bits: Bits) -> Bits:
    mutation_probability = 1 / n
    chance = random()
    if chance >= mutation_probability:
        return bits
    copy = deepcopy(bits)
    i = randint(0, n - 1)
    copy[i] = __flip(bits[i])
    return copy


def __terminate(n: int, individual: Individual[Bits], generation: int) -> bool:
    return generation == n * 100 or individual.fitness == n


solve_max_sum_bits = genetic(
    __population, __fitness, __crossover, __mutate, __terminate
)
