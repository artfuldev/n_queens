from typing import Tuple


Board = list[int]
Index = Tuple[int, int]


def has_collision(board: Board, x: int, y: int) -> bool:
    x_queen = board[x]
    y_queen = board[y]
    if x_queen == y_queen:
        return True
    row_diff = x - y
    col_diff = x_queen - y_queen
    return row_diff == col_diff or row_diff == -col_diff


def colliding_indices(board: Board) -> list[Index]:
    size = len(board)
    indices: list[Index] = []
    for x in range(size):
        for y in range(size):
            if x != y and has_collision(board, x, y):
                indices.append([x, y])
    return indices


def __stringify_row(size: int, row: int):
    col_strings = []
    for i in range(size):
        col_strings.append("Q" if i == row else "_")
    return " ".join(col_strings)


def stringify(board: Board):
    size = len(board)
    row_strings = []
    for row in board:
        row_strings.append(__stringify_row(size, row))
        row_strings.append("\n")
    return "".join(row_strings)
