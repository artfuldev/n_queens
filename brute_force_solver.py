from board import Board


def solve_row(board: Board, row: int):
    solutions: list[Board] = []
    board_size = board.size()
    if row >= board_size:
        solutions.append(board)
        return solutions
    col = 0
    while col < board_size:
        board = board.place(row, col)
        if board.is_valid():
            for solution in solve_row(board, row + 1):
                solutions.append(solution)
        col += 1
    return solutions


def solve_row_first(board: Board, row: int):
    board_size = board.size()
    solution: Board | None = None
    if row >= board_size:
        return board
    col = 0
    while col < board_size:
        board = board.place(row, col)
        if board.is_valid():
            solution = solve_row_first(board, row + 1)
            if solution is not None:
                return solution
        col += 1
    return solution


def solve(board_size):
    return solve_row(Board.empty(board_size), 0)


def solve_first(board_size):
    return solve_row_first(Board.empty(board_size), 0)
