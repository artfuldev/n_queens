from copy import copy


NO_QUEEN_PLACED = -1


def remove_queen(board, row):
    new_board = copy(board)
    new_board[row] = NO_QUEEN_PLACED
    return new_board


def place_queen(board, row, col):
    new_board = copy(board)
    new_board[row] = col
    return new_board


def sprint_board(board):
    board_sprint = []
    for row in board:
        row_sprint = []
        for i in range(len(board)):
            row_sprint.append("Q" if i == row else "_")
        board_sprint.append(" ".join(row_sprint))
    return "\n".join(board_sprint) + "\n"


def has_collision(board, x, y):
    if board[x] == NO_QUEEN_PLACED or board[y] == NO_QUEEN_PLACED:
        return False
    if board[x] == board[y]:
        return True
    difference = x - y
    board_difference = board[x] - board[y]
    return difference == board_difference or difference == -board_difference


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
    board = [NO_QUEEN_PLACED for i in range(board_size)]
    return board
