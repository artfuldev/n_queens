from copy import copy
from random import shuffle


def place_queen(board: list[int | None], row: int, col: int):
    new_board = copy(board)
    new_board[row] = col
    return new_board


def empty(size: int):
    return [None for row in range(size)]


def filled(size: int):
    board: list[int] = [None for row in range(size)]
    positions = list(range(size))
    shuffle(positions)
    for row in range(size):
        board = place_queen(board, row, positions[row])
    return board


def has_collision(board: list[int | None], x: int, y: int):
    x_queen = board[x]
    y_queen = board[y]
    if x_queen is None or y_queen is None:
        return False
    if x_queen == y_queen:
        return True
    row_diff = x - y
    col_diff = x_queen - y_queen
    return row_diff == col_diff or row_diff == -col_diff


def colliding_indices(board: list[int | None], size: int):
    indices: list[list[int]] = []
    for x in range(size):
        for y in range(size):
            if x != y and has_collision(board, x, y):
                indices.append([x, y])
    return indices


def swap(board: list[int | None], x: int, y: int):
    with_new_x = place_queen(board, x, board[y])
    with_new_y = place_queen(with_new_x, y, board[x])
    return with_new_y
