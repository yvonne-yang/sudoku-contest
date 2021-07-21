import numpy as np
from abc import ABC

class SudokuSolver(ABC):
'''
Abstract baseclass for sudoku solver class, inherited methods for solution routine
Define your child class as "class _____(SudokuSolver):" and remember to call super constructor!
'''
    def __init__(self):
        self.ROWS = 9
        self.COLS = 9
        self.puzzle = None
        self.solve_time = None

    # initialize puzzle from single string tdoku format. Limited input checks, so be careful
    def init_puzzle(self, puzzle_input: str) -> bool:
        # some input checks
        if len(puzzle) != 81:
            return False
        # make numpy array to store puzzle, initialized to -1
        self.puzzle = np.zeros((9,9)) - 1
        # unpack text representation of puzzle into internal array
        for rowidx in range(self.ROWS):
            for colidx in range(self.COLS):
                if puzzle_input[rowidx*self.COLS + colidx] is not '.':
                    self.puzzle[rowidx, colidx] = int(puzzle_input[rowidx*self.COLS + colidx])
        # return success
        return True

    # returns the tdoku string formatted puzzle at its current state, can be called on internal state puzzle or another in same form
    def get_puzzle_string(self, puzzle=self.puzzle) -> str:
        # make string to hold tdoku formatted puzzle
        fmted_puzzle = ''
        # loop through array in row-major fashion, use '.' as null spot
        for rowidx in range(self.ROWS):
            for colidx in range(self.COLS):
                fmted_puzzle += str(puzzle[rowidx, colidx]) if puzzle[rowidx, colidx] is not -1 else '.'
        # return formatted string representation of puzzle
        return fmted_puzzle

    # get value of item at given row and column in internal puzzle
    def get_index(self, row: int, col: int) -> int:
        return self.puzzle[row, col]

    # core forwardchecking algorithm to determine whether a spot can hold a value
    def index_can_have(self, row: int, col: int, value: int) -> bool:
        # check whether the row, column, or box of the index has a certain value
        can_have = not (row_has(row, value) or column_has(col, value) or box_has(row, col, value))
        # return whether the queried index can have the value
        return can_have

    # get whether a number exists in given row (unneeded if you rely on 'index_can_have' instead)
    def row_has(self, row: int, value: int) -> bool:
        # check whether any values in the row are the target value
        if np.any(self.puzzle[row, :] == value):
            return True
        else:
            return False

    # get whether a number exists in given column (unneeded if you rely on 'index_can_have' instead)
    def column_has(self, col: int, value: int) -> bool:
        # check whether any values in the column are the target value
        if np.any(self.puzzle[:, col] == value):
            return True
        else:
            return False

    # test whether the box corresponding to a given index has a value
    def box_has(self, row: int, col: int, value: int) -> bool:
        if row < 3:
            # box 1
            if col < 3:
                if np.any(self.puzzle[:3, :3] == value):
                    return True
            # box 2
            elif col < 6:
                if np.any(self.puzzle[:3, 3:6] == value):
                    return True
            # box 3
            else:
                if np.any(self.puzzle[:3, 7:] == value):
                    return True
        elif row < 6:
            # box 4
            if col < 3:
                if np.any(self.puzzle[3:6:, :3] == value):
                    return True
            # box 5
            elif col < 6:
                if np.any(self.puzzle[3:6, 3:6] == value):
                    return True
            # box 6
            else:
                if np.any(self.puzzle[3:6, 7:] == value):
                    return True
        else:
            # box 7
            if col < 3:
                if np.any(self.puzzle[7:, :3] == value):
                    return True
            # box 8
            elif col < 6:
                if np.any(self.puzzle[7:, 3:6] == value):
                    return True
            # box 9
            else:
                if np.any(self.puzzle[7:, 7:] == value):
                    return True
        # return false if no conditionals were triggered (for readability)
        return False
    
    @abstractmethod
    def solve_puzzle(self) -> bool:
        # should return a boolean value for whether the puzzle was solved successfully or not
        pass

    def print_puzzle(self) -> None:
        # print little header message
        print('\nCurrent Puzzle State')
        # loop through rows and columns and print one row at a time
        for rowidx in range(self.ROWS):
            # print horizontal lines
            if rowidx == 3 or rowidx == 6:
                print('-'*(self.COLS+2))
            for colidx in range(self.COLS)
                # print vertical lines
                if colidx == 3 or colidx == 6:
                    print('|')
                # print number
                print(str(self.puzzle[rowidx, colidx]))
