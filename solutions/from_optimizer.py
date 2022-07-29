from functools import reduce
from algorithms.distinct import distinct
from algorithms.from_optimizer import from_optimizer as from_optimize
from algorithms.infinite import infinite
from algorithms.optimize import Optimize
from algorithms.solve import Solve
from algorithms.transform import Transform
from algorithms.valid import valid
from algorithms.with_transpositions import with_transpositions
from domain.board import Board, Size, cache_key, collisions, transpositions


def __valid(n: Size, board: Board) -> bool:
    return collisions(n, board) == 0


def __key(n: Size, board: Board) -> str:
    return cache_key(board)


def from_optimizer(optimize: Optimize[Size, Board]) -> Solve[Size, Board]:
    transformers: list[Transform[Size, Board]] = [
        infinite,
        valid(__valid),
        with_transpositions(transpositions),
        distinct(__key),
    ]
    return reduce(lambda g, t: t(g), transformers, from_optimize(optimize))
