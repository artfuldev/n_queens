from timeit import default_timer
from brute_force_solver import solve_first

for size in range(15, 16):
    tic = default_timer()
    first_solution = solve_first(size)
    toc = default_timer()
    seconds = toc - tic
    if first_solution is not None:
        print("1 solution for {}x{} board found in {:0.3f}s".format(size, size, seconds))
        print(first_solution.stringify())
    else:
        print("No solution found for {}x{} board in {:0.3f}s".format(size, size, seconds))
