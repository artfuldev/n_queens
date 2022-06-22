from timeit import default_timer
from brute_force_solver import solve_first
from board import sprint_board

for size in range(8, 9):
    tic = default_timer()
    first_solution = solve_first(size)
    toc = default_timer()
    print("1 solution for {}x{} board found in {:0.3f}s".format(size, size, toc - tic))
    print(sprint_board(first_solution))
