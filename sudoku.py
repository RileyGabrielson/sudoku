import numpy as np


class Cell:
    def __init__(self, max_val=9):
        self.possibleValues = [i for i in range(1, max_val+1)]
        self.actualValue = None

    def remove_possible(self, value):
        if len(self.possibleValues) == 1:
            return

        if value in self.possibleValues:
            self.possibleValues.remove(value)

        if len(self.possibleValues) == 1:
            self.actualValue = self.possibleValues[0]

    def set_actual(self, value):
        self.actualValue = value
        self.possibleValues = [value]

    def __str__(self):
        return str(self.actualValue)


class Board:
    def __init__(self, max_val=9, known_vals=[]):
        self.cells = np.array([[Cell(max_val=max_val)
                              for j in range(max_val)] for i in range(max_val)])

        self.max_val = max_val
        self.square_length = int(np.sqrt(max_val))

        if len(known_vals) > 0:
            for i in range(len(known_vals)):
                for j in range(len(known_vals[0])):
                    if known_vals[i, j] != None:
                        self.set_cell_value(j, i, known_vals[i, j])

    def set_cell_value(self, x, y, val):
        self.cells[y, x].set_actual(val)

    def remove_possibles(self, x, y):
        val = self.cells[y, x].actualValue
        if val == None:
            return

        # Remove option in column
        for cell in self.cells[:, x]:
            cell.remove_possible(val)

        # Remove option in row
        for cell in self.cells[y, :]:
            cell.remove_possible(val)

        # Remove option in square
        square_x = int(x / self.square_length)
        square_y = int(y / self.square_length)
        for i in range(square_x * self.square_length, (square_x + 1) * self.square_length):
            for j in range(square_y * self.square_length, (square_y + 1) * self.square_length):
                self.cells[j, i].remove_possible(val)

    def is_solved(self):
        for row in self.cells:
            vals = set()
            for cell in row:
                vals.add(cell.actualValue)
            if None in vals or len(vals) != self.max_val:
                return False

        for column in self.cells.T:
            vals = set()
            for cell in column:
                vals.add(cell.actualValue)
            if None in vals or len(vals) != self.max_val:
                return False

        for square_y in range(self.square_length):
            for square_x in range(self.square_length):
                square = self.cells[(square_y * self.square_length):((square_y + 1) * self.square_length),
                                    (square_x * self.square_length):((square_x + 1) * self.square_length)].flatten()
                vals = set()
                for cell in square:
                    vals.add(cell.actualValue)
                if None in vals or len(vals) != self.max_val:
                    return False

        return True

    def to_array(self):
        return np.array([[self.cells[i, j].actualValue for j in range(len(self.cells[0]))] for i in range(len(self.cells))])

    def __str__(self):
        return str(np.array([[str(self.cells[i, j]) for j in range(len(self.cells[0]))] for i in range(len(self.cells))]))
