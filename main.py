# board of size n x n
# n = number of queens and also size of board

import sys
from random import choice
from timeit import default_timer

def remove_queen(board, row, col):
    board[row][col] = 0


def place_queen(board, row, col):
    board[row][col] = 1


def print_board(board):
    for row in board:
        print(row)

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
    if row >= board_size:
        return True
    col = 0
    while col < board_size:
        place_queen(board, row, col)
        if is_valid_board(board):
            if solve_row(board, row + 1):
                return True
        remove_queen(board, row, col)
        col += 1
    return False


def solve(board_size):
    board = [[0 for i in range(board_size)] for j in range(board_size)]
    solve_row(board, 0)
    print("The solved board is:")
    print_board(board)


def main():
    n = int(input("Enter the size of the board: "))
    solve(n)

for size in range(4, 101):
    tic = default_timer()
    solve(size)
    toc = default_timer()
    print("Time taken to solve {}x{} board: {}".format(size, size, toc - tic))
