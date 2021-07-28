import numpy as np

# this class checks the correctness of a sudoku solution given a set of clues (constraints)
class SolutionConsistencyChecker:
    def __init__(self):
        self.ROWS = 9
        self.COLS = 9
        self.puzzle = None
        self.clues = None

    # initialize puzzle from single string tdoku format. Limited input checks, so be careful
    def check_puzzle(self, puzzle_input: str, puzzle_clues: str) -> bool:
        # make numpy array to store puzzle, initialized to -1
        self.puzzle = np.zeros((9,9))
        # unpack text representation of puzzle into internal array
        for rowidx in range(self.ROWS):
            for colidx in range(self.COLS):
                if puzzle_input[rowidx*self.COLS + colidx] != '.':
                    self.puzzle[rowidx, colidx] = int(puzzle_input[rowidx*self.COLS + colidx])
                else:
                    return False

        # make numpy array to store puzzle, initialized to -1
        self.clues = np.zeros((9,9)) - 1
        # unpack text representation of puzzle into internal array
        for rowidx in range(self.ROWS):
            for colidx in range(self.COLS):
                if puzzle_clues[rowidx*self.COLS + colidx] != '.':
                    self.clues[rowidx, colidx] = int(puzzle_clues[rowidx*self.COLS + colidx])
        
        # store boolean for proper solution
        consistent_sol = True

        # check against clues and that all are solved
        consistent_sol = consistent_sol and self.check_against_clues()

        # check to make sure each partition has a value once
        for value in np.arange(start=1, stop=10):
            # check rows
            for row in np.arange(start=0, stop=9):
                consistent_sol = consistent_sol and (count_along_row(row, value) == 1)
            # check columns
            for col in np.arange(start=0, stop=9):
                consistent_sol = consistent_sol and (count_along_column(col, value) == 1)
            # check boxes
            for box_row in np.arange(start=0, stop=3):
                for box_col in np.arange(start=0, stop=3):
                    consistent_sol = consistent_sol and (count_inside_box(box_row, box_col, value) == 1)
        
        return consistent_sol

    # check to make sure each cell in clue matches solution or was not given
    def check_against_clues(self) -> bool:
        return np.all(self.puzzle == self.clues or self.clues == -1)

    # count a given value along a row
    def count_along_row(self, rowidx: int, value: int) -> int:
        return (self.puzzle[rowidx, :] == value).sum()

    # count a given value along a column
    def count_along_column(self, colidx: int, value: int) -> int:
        return (self.puzzle[:, colidx] == value).sum()
        
    # count a given value inside a box
    def count_inside_box(self, box_row: int, box_col: int, value: int) -> bool:
        if box_row == 0:
            # box 1
            if box_col == 0:
                return (self.puzzle[:3, :3] == value).sum()
            # box 2
            elif box_col == 1:
                return (self.puzzle[:3, 3:6] == value).sum()
            # box 3
            else:
                return (self.puzzle[:3, 7:] == value).sum()
        elif box_row == 1:
            # box 4
            if box_col == 0:
                return (self.puzzle[3:6:, :3] == value).sum()
            # box 5
            elif box_col == 1:
                return (self.puzzle[3:6, 3:6] == value).sum()
            # box 6
            else:
                return (self.puzzle[3:6, 7:] == value).sum()
        else:
            # box 7
            if box_col == 0:
                return (self.puzzle[7:, :3] == value).sum()
            # box 8
            elif box_col == 1:
                return (self.puzzle[7:, 3:6] == value).sum()
            # box 9
            else:
                return (self.puzzle[7:, 7:] == value).sum()
