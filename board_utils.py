from copy import copy


def place_queen(board: list[int], row: int, col: int):
    new_board = copy(board)
    new_board[row] = col
    return new_board


def has_collision(board: list[int], x: int, y: int):
    x_queen = board[x]
    y_queen = board[y]
    if x_queen is None or y_queen is None:
        return False
    if x_queen == y_queen:
        return True
    row_diff = x - y
    col_diff = x_queen - y_queen
    return row_diff == col_diff or row_diff == -col_diff


def colliding_indices(board: list[int], size: int):
    indices: list[list[int]] = []
    for x in range(size):
        for y in range(size):
            if x != y and has_collision(board, x, y):
                indices.append([x, y])
    return indices


def swap(board: list[int], x: int, y: int):
    with_new_x = place_queen(board, x, board[y])
    with_new_y = place_queen(with_new_x, y, board[x])
    return with_new_y
