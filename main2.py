from itertools import islice
from solutions.sum_of_n_bits import solve_max_sum_bits

for bits in islice(solve_max_sum_bits(20), 100):
    print(bits)
