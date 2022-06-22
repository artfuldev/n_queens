from copy import copy


def queen_at(board, row):
    return board[row]


def place_queen(board, row, col):
    new_board = copy(board)
    new_board[row] = col
    return new_board


def stringify_row(size, row):
    col_strings = []
    for i in range(size):
        col_strings.append("Q" if i == row else "_")
    return " ".join(col_strings)


def stringify(board):
    size = len(board)
    row_strings = []
    for row in board:
        row_strings.append(stringify_row(size, row))
    return "\n".join(row_strings) + "\n"


def has_collision(board, x, y):
    x_queen = queen_at(board, x)
    y_queen = queen_at(board, y)
    if x_queen is None or y_queen is None:
        return False
    if x_queen == y_queen:
        return True
    row_diff = x - y
    col_diff = x_queen - y_queen
    return row_diff == col_diff or row_diff == -col_diff


def collisions(board):
    collisions = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if x != y and has_collision(board, x, y):
                collisions += 1
    return collisions


def is_valid_board(board):
    return collisions(board) == 0


def create(board_size):
    board = [None for i in range(board_size)]
    return board
