# board of size n x n
# n = number of queens and also size of board

import sys
from random import choice
from timeit import default_timer
from copy import deepcopy


def set_value(board, row, col, value):
    new_board = deepcopy(board)
    new_board[row][col] = value
    return new_board


def remove_queen(board, row, col):
    return set_value(board, row, col, 0)


def place_queen(board, row, col):
    return set_value(board, row, col, 1)


def sprint_cell(cell):
    return "Q" if cell == 1 else "_"


def sprint_row(row):
    row_sprint = []
    for cell in row:
        row_sprint.append(sprint_cell(cell))
    return " ".join(row_sprint)


def sprint_board(board):
    board_sprint = []
    for row in board:
        board_sprint.append(sprint_row(row))
    return "\n".join(board_sprint)


def print_board(board):
    print(sprint_board(board))
    print('')


def print_board_as_string(board):
    string = ""
    for row in board:
        string += str(row)
        string += "\n"
    return string


def is_valid_row(board, row):
    count = 0
    for col in range(len(board)):
        count += board[row][col]
        if count > 1:
            return False
    return True


def is_valid_col(board, col):
    count = 0
    for row in range(len(board)):
        count += board[row][col]
        if count > 1:
            return False
    return True


def is_valid_diag(board, row, col):
    count_left = 0
    count_right = 0
    for i in range(len(board)):
        if row + i < len(board) and col + i < len(board):
            count_left += board[row + i][col + i]
            if count_left > 1:
                return False
        if row - i >= 0 and col + i < len(board):
            count_right += board[row - i][col + i]
            if count_right > 1:
                return False
    return True


def is_valid_board(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 1:
                if (
                    not is_valid_row(board, row)
                    or not is_valid_col(board, col)
                    or not is_valid_diag(board, row, col)
                ):
                    return False
    return True


def solve_row(board, row):
    board_size = len(board)
    solutions = []
    if row >= board_size:
        solutions.append(board)
        return solutions
    col = 0
    while col < board_size:
        board = place_queen(board, row, col)
        if is_valid_board(board):
            for solution in solve_row(board, row + 1):
                solutions.append(solution)
        board = remove_queen(board, row, col)
        col += 1
    return solutions


def solve(board_size):
    board = [[0 for i in range(board_size)] for j in range(board_size)]
    solutions = solve_row(board, 0)
    return solutions


def main():
    n = int(input("Enter the size of the board: "))
    solve(n)


for size in range(4, 101):
    tic = default_timer()
    solutions = len(solve(size))
    toc = default_timer()
    print("{} solutions for {}x{} board found in {:0.3f}s".format(solutions, size, size, toc - tic))