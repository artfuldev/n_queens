from random import choice, choices, shuffle
from typing import Tuple, cast
from algorithms.particle_swarm import Plan, Components, particle_swarm as algorithm
from domain.board import Column, Row, Size, Board, cache_key, colliding_row_pairs, swap
from domain.list import flatten, unique


def __board(n: Size) -> Board:
    board = Board(list(map(Column, range(n))))
    shuffle(board)
    return board


def __first(n: Size) -> list[Board]:
    return [__board(n) for _ in range(n)]


def __velocity(n: Size, board: Board) -> Tuple[Row, Row]:
    pairs = colliding_row_pairs(n, board)
    if len(pairs) == 0:
        return cast(Tuple[Row, Row], choices(list(map(Row, range(n))), k=2))
    x, y = choice(pairs)
    not_x_or_y = lambda i: i not in (x, y)
    y_choices = list(filter(not_x_or_y, unique(flatten(cast(list[list[Row]], pairs)))))
    if len(y_choices) == 0:
        y_choices = [y]
    return (x, choice(y_choices))


def __quality(n: Size, board: Board) -> float:
    return (pow(n, 2) - len(colliding_row_pairs(n, board))) * 100 / pow(n, 2)


def __terminate(n: Size, board: Board) -> bool:
    return __quality(n, board) == 100


def __cognitive(n: Size, positions: Plan[Board]) -> Tuple[Row, Row]:
    pass

def __social(n: Size, positions: Plan[Board]) -> Tuple[Row, Row]:
    pass

def __next(n: Size, components: Components[Tuple[Row, Row]]) -> Tuple[Row, Row]:
    pass

def __apply(n: Size, board: Board, row_pair: Tuple[Row, Row]):
    x, y = row_pair
    return swap(board, x, y)

def __cache_key(_: Size, board: Board) -> str:
    return cache_key(board)


particle_swarm = algorithm(
    __first,
    __velocity,
    __quality,
    __terminate,
    __cognitive,
    __social,
    __next,
    __apply,
    __cache_key,
)
