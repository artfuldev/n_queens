from timeit import default_timer
from models.board import Board, stringify
from n_queens_solvers.brute_force import solve
from int_utils import nth


def find_solutions(size: int, count: int, until: int = None):
    stop = size + 1 if until is None else until + 1
    for n in range(size, stop):
        tic = default_timer()
        if count <= 0:
            raise
        solutions: list[Board] = []
        tic = default_timer()
        solutions_generator = solve(n)
        for i in range(count):
            solution = next(solutions_generator, None)
            if solution is None:
                break
            else:
                solutions.append(solution)
        toc = default_timer()
        seconds = toc - tic
        solutions_count = len(solutions)
        if solutions_count != 0:
            print(
                "{} solution{} for {}x{} board found in {:0.3f}s".format(
                    solutions_count,
                    "s" if solutions_count > 1 else "",
                    n,
                    n,
                    seconds,
                )
            )
            print(
                "{} solution\n{}".format(nth(solutions_count), stringify(solutions[-1]))
            )
        else:
            print("No solution found for {}x{} board in {:0.3f}s".format(n, n, seconds))


find_solutions(4, 100, 8)
