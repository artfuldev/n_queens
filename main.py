from timeit import default_timer
from brute_force_solver import solve

for size in range(15, 16):
    tic = default_timer()
    solution = next(solve(size), None)
    toc = default_timer()
    seconds = toc - tic
    if solution is not None:
        print("1 solution for {}x{} board found in {:0.3f}s".format(size, size, seconds))
        print(solution.stringify())
    else:
        print("No solution found for {}x{} board in {:0.3f}s".format(size, size, seconds))
