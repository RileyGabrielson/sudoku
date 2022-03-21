from matplotlib.axis import YAxis
import numpy as np
from sudoku import Board
from itertools import combinations


class SudokuSolver:
    def __init__(self, max_val=9, known_vals=[]):
        self.board = Board(max_val=max_val, known_vals=known_vals)

    def add_critical_row_values(self, y):
        row = self.board.cells[y, :]
        for val in range(1, self.board.max_val + 1):
            only_valid_cell_in_row = None
            multiple_options = False
            for cell in row:
                if val in cell.possibleValues and only_valid_cell_in_row == None:
                    only_valid_cell_in_row = cell
                elif val in cell.possibleValues and only_valid_cell_in_row != None:
                    multiple_options = True

            if not multiple_options:
                only_valid_cell_in_row.set_actual(val)

    def add_critical_column_values(self, x):
        column = self.board.cells[:, x]
        for val in range(1, self.board.max_val + 1):
            only_valid_cell_in_column = None
            multiple_options = False
            for cell in column:
                if val in cell.possibleValues and only_valid_cell_in_column == None:
                    only_valid_cell_in_column = cell
                elif val in cell.possibleValues and only_valid_cell_in_column != None:
                    multiple_options = True

            if not multiple_options:
                only_valid_cell_in_column.set_actual(val)

    def add_critical_square_values(self, square_x, square_y):
        square = self.board.cells[(square_y * self.board.square_length):((square_y + 1) * self.board.square_length),
                                  (square_x * self.board.square_length):((square_x + 1) * self.board.square_length)].flatten()
        for val in range(1, self.board.max_val + 1):
            only_valid_cell_in_square = None
            multiple_options = False
            for cell in square:
                if val in cell.possibleValues and only_valid_cell_in_square == None:
                    only_valid_cell_in_square = cell
                elif val in cell.possibleValues and only_valid_cell_in_square != None:
                    multiple_options = True

            if not multiple_options:
                only_valid_cell_in_square.set_actual(val)

    def closed_loops_row(self, y, max_comb_length=4):
        row = self.board.cells[y, :]
        for i in range(2, max_comb_length + 1):
            subsets = combinations(row, i)
            for subset in subsets:
                vals = set()
                for cell in subset:
                    vals.add(cell.actualValue)
                if not None in vals and len(vals) == i:
                    print("we need to do something here to remove the possibles")

    def smart_solve(self):
        solved = False
        max_iter = 50
        iter = 0

        while not solved and iter < max_iter:
            iter += 1
            for i in range(len(self.board.cells)):
                for j in range(len(self.board.cells[0])):
                    self.board.remove_possibles(i, j)

            for y in range(len(self.board.cells)):
                self.add_critical_row_values(y)

            for x in range(len(self.board.cells[0])):
                self.add_critical_column_values(x)

            for x in range(self.board.square_length):
                for y in range(self.board.square_length):
                    self.add_critical_square_values(x, y)

            num_none_values = np.sum(np.array([[self.board.cells[i, j].actualValue == None for j in range(
                len(self.board.cells[0]))] for i in range(len(self.board.cells))]))
            solved = num_none_values == 0

    def brute_solve(self):
        array = self.board.to_array()
        return self._brute_recursive(array, 0, 0)

    def _brute_recursive(self, cur_array, cur_x, cur_y):
        if cur_x == self.board.max_val - 1 and cur_y == self.board.max_val - 1:
            for possible in self.board.cells[cur_y, cur_x].possibleValues:
                copy = np.copy(cur_array)
                copy[cur_y, cur_x] = possible
                temp_board = Board(max_val=self.board.max_val,
                                   known_vals=copy)
                solved = temp_board.is_solved()
                if solved:
                    return True, temp_board.to_array()
            return False, cur_array

        y = cur_y + 1
        x = cur_x
        if y >= len(cur_array):
            y = 0
            x += 1

        if cur_array[cur_y, cur_x] == None:
            for possible in self.board.cells[cur_y, cur_x].possibleValues:
                copy = np.copy(cur_array)
                copy[cur_y, cur_x] = possible
                solved, solution_array = self._brute_recursive(copy, x, y)
                if solved:
                    return True, solution_array
        else:
            return self._brute_recursive(cur_array, x, y)

        return False, cur_array

    def solve(self):
        self.smart_solve()
        if not self.board.is_solved():
            self.brute_solve()

        return self.board.to_array()
