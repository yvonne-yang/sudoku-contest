import numpy as np

# this class checks the correctness of a sudoku solution given a set of clues (constraints)
class SolutionConsistencyChecker:
    def __init__(self, debug=False):
        self.ROWS = 9
        self.COLS = 9
        self.puzzle = None
        self.clues = None

        # set debug mode for more advanced error messages, useful when developing solvers
        self.debugmode = debug

    # initialize puzzle from single string tdoku format. Limited input checks, so be careful
    def check_puzzle(self, puzzle_input: str, puzzle_clues: str) -> bool:
        # print message if currently in debug mode
        if self.debugmode:
            print('\nCONSISTENCY CHECKER SET TO DEBUG MODE')
            print('submitted solution string:\n',puzzle_input)
            print('submitted clue string:\n',puzzle_clues)
        # make numpy array to store puzzle, initialized to -1
        self.puzzle = np.zeros((9,9))
        # unpack text representation of puzzle into internal array
        for rowidx in range(self.ROWS):
            for colidx in range(self.COLS):
                if puzzle_input[rowidx*self.COLS + colidx] != '.':
                    self.puzzle[rowidx, colidx] = int(puzzle_input[rowidx*self.COLS + colidx])
                else:
                    if self.debugmode:
                        print(f'UNWRITTEN ERROR: not all cells are assigned a value: cell {rowidx},{colidx} was unassigned')
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
        if self.debugmode and not consistent_sol:
            print('CLUE ERROR: a clue was detected to be overwritten')

        # perform value checking for rows, columns, and boxes
        consistent_sol = consistent_sol and self.check_cell_values()
        if self.debugmode and not consistent_sol:
            self.debug_cell_errors()

        return consistent_sol

    # check all cell values and return total correctness
    def check_cell_values(self) -> bool:
        # store boolean to contain cell correctness
        consistent_sol = True

        # check to make sure each partition has a value once
        for value in np.arange(start=1, stop=10):
            # check rows
            for row in np.arange(start=0, stop=9):
                consistent_sol = consistent_sol and (self.count_along_row(row, value) == 1)
            # check columns
            for col in np.arange(start=0, stop=9):
                consistent_sol = consistent_sol and (self.count_along_column(col, value) == 1)
            # check boxes
            for box_row in np.arange(start=0, stop=3):
                for box_col in np.arange(start=0, stop=3):
                    consistent_sol = consistent_sol and (self.count_inside_box(box_row, box_col, value) == 1)

        # return accumulated cell checks
        return consistent_sol

    # check to make sure each cell in clue matches solution or was not given
    def check_against_clues(self) -> bool:
        return np.all(np.logical_or(self.puzzle == self.clues, self.clues == -1))

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

    # small debug script to point out errors in cells
    def debug_cell_errors(self) -> None:
        # print stats for values written to solved puzzle
        print('\nContents of the failed solution were as follows:')
        unique, counts = np.unique(self.puzzle, return_counts=True)
        print(f'\t{dict(zip(unique, counts))}')
        # check to make sure each partition has a value once
        for value in np.arange(start=1, stop=10):
            # check rows
            for row in np.arange(start=0, stop=9):
                if self.count_along_row(row, value) != 1:
                    print(f'ROW ERROR: {self.count_along_row(row, value)} occurrences of {value} in row {row}')
            # check columns
            for col in np.arange(start=0, stop=9):
                if self.count_along_column(col, value) != 1:
                    print(f'COLUMN ERROR: {self.count_along_column(col, value)} occurrences of {value} in column {col}')
            # check boxes
            for box_row in np.arange(start=0, stop=3):
                for box_col in np.arange(start=0, stop=3):
                    if self.count_inside_box(box_row, box_col, value) != 1:
                        print(f'BOX ERROR: {self.count_inside_box(box_row, box_col, value)} occurrences of {value} in box ({box_row},{box_col})')

if __name__ == "__main__":
    # sets of values intended to raise errors
    cluevalues = '1'*81
    unwrittenerror = '.'*81
    clueerror = '2'*81
    cellerror = '1'*81
    # STILL NEED A CORRECT PUZZLE TO TRY TO SEE IF IT WORKS

    # make solution checker with debug=True
    solution_checker = SolutionConsistencyChecker(debug=True)

    # raise each type of consistency error
    solution_checker.check_puzzle(unwrittenerror, cluevalues)
    solution_checker.check_puzzle(clueerror, cluevalues)
    solution_checker.check_puzzle(cellerror, cluevalues)

