from solver import SudokuSolver
import numpy as np

init_vals_easy = np.array([
    [None, None, 3, None, 7, 2, 4, None, 9],
    [None, 9, None, None, None, 1, 7, 5, 2],
    [None, 7, None, 5, None, None, None, None, 6],
    [None, 3, None, 2, 8, 4, 6, None, None],
    [2, None, 1, 3, None, None, None, 4, None],
    [None, 6, 9, 1, None, 7, None, None, None],
    [9, None, 6, 4, 1, None, None, None, None],
    [1, None, None, None, 6, None, 9, 2, None],
    [3, None, 7, None, None, None, 1, None, 5],
])

init_vals_evil = np.array([
    [None, None, None, 1, None, None, None, None, None],
    [None, None, 9, None, 5, 6, None, None, 8],
    [None, 3, None, None, None, None, None, 4, None],
    [None, None, 6, None, 7, 8, None, None, 5],
    [None, None, None, None, None, 2, None, None, None],
    [9, None, None, None, None, None, 6, None, None],
    [None, None, None, 9, None, None, None, None, 1],
    [4, None, None, None, 1, 7, None, 8, None],
    [None, None, 7, 2, None, None, None, None, None]
])


my_solver = SudokuSolver(known_vals=init_vals_evil)
solved, solution = my_solver.brute_solve()
print(solved)
print(solution)
