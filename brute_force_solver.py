from board import create, place_queen, remove_queen, is_valid_board


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


def solve_row_first(board, row):
    board_size = len(board)
    solution = None
    if row >= board_size:
        return board
    col = 0
    while col < board_size:
        board = place_queen(board, row, col)
        if is_valid_board(board):
            solution = solve_row_first(board, row + 1)
            if solution is not None:
                return solution
        board = remove_queen(board, row)
        col += 1
    return solution


def solve(board_size):
    return solve_row(create(board_size), 0)


def solve_first(board_size):
    return solve_row_first(create(board_size), 0)
