from board import Board
from typing import Generator


def __solve(board: Board, row: int) -> Generator[Board, None, None]:
    board_size = board.size()
    if row >= board_size:
        yield board
    else:
        col = 0
        while col < board_size:
            board = board.place(row, col)
            if board.is_valid_until(row):
                for solution in __solve(board, row + 1):
                    yield solution
            col += 1

def solve(size: int):
    return __solve(Board(size), 0)
