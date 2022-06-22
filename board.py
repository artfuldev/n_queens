from copy import copy


def queen_at(board, row):
    return board[row]


def remove_queen(board, row):
    new_board = copy(board)
    new_board[row] = None
    return new_board


def place_queen(board, row, col):
    new_board = copy(board)
    new_board[row] = col
    return new_board


def sprint_row(size, row):
    row_sprint = []
    for i in range(size):
        row_sprint.append("Q" if i == row else "_")
    return " ".join(row_sprint)


def sprint_board(board):
    size = len(board)
    board_sprint = []
    for row in board:
        board_sprint.append(sprint_row(size, row))
    return "\n".join(board_sprint) + "\n"


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
