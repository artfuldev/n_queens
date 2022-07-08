from itertools import islice
from domain.board import Size
from solutions.genetic import genetic

for solution in islice(genetic(Size(8)), 92):
    print(solution)
