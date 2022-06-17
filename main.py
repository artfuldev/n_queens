# board of size n x n
# n = number of queens and also size of board


from random import choice


def remove_queen(board, row, col):
    board[row][col] = 0


def place_queen(board, row, col):
    board[row][col] = 1


def print_board(board):
    for row in board:
        print(row)


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


def solve(board_size):
    board = [[0 for i in range(board_size)] for j in range(board_size)]

    last_col_indices = []
    last_row_index = 0
    valid_col_indices = {}
    visited_col_indices = {}
    row_index = 0
    col_index = 0
    backtracked_row_indices = []

    for i in range(board_size):
        valid_col_indices[i] = []
        visited_col_indices[i] = []

    while row_index < board_size:
        while col_index < board_size:
            print(f"row: {row_index} col: {col_index}")
            place_queen(board, row_index, col_index)
            if is_valid_board(board):
                print("valid")
                valid_col_indices[row_index].append(col_index)
                last_row_index = row_index
                last_col_indices.append(col_index)
                row_index += 1
                col_index = 0
            else:
                print("invalid")
                remove_queen(board, row_index, col_index)
                col_index += 1
                if col_index == board_size:
                    remove_queen(board, last_row_index, last_col_indices[-1])
                    col_index = last_col_indices.pop() + 1
                    
                    while last_row_index in backtracked_row_indices:
                        last_row_index -= 1
                        
                    row_index = last_row_index
                    col_index = last_col_indices[row_index] + 1

                    while col_index >= board_size:
                        row_index -= 1
                        col_index = last_col_indices[row_index] + 1
                    backtracked_row_indices.append(last_row_index)

    print("The solved board is:")
    print_board(board)


def main():
    n = int(input("Enter the size of the board: "))
    solve(n)


# board = [[0 for i in range(4)] for j in range(4)]
# board[0][2] = 1
# board[1][0] = 1
# board[2][3] = 1
# board[3][1] = 1

# print(is_valid_row(board, 0))
# print(is_valid_col(board, 0))
# print(is_valid_diag(board, 0, 2))
# print(is_valid_board(board))
solve(8)
