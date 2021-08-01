import numpy as np
from SudokuSolverBase import SudokuSolver

class j_wilkes_b(SudokuSolver):
    def __init__(self):
        # flag for unsolveable puzzle
        self.unsolvable = False
        super().__init__()

    def solve_puzzle(self):
        # lower unsolveable flag
        self.unsolveable = False

        # cell counter
        current_cell = 0
        current_value = 1
        rewind = False
        
        # keep going until all the rows are solved
        while current_cell < self.ROWS * self.COLS:
            # print running value of puzzle
            print(self.get_puzzle_string(), end="\r")

            # get current position
            current_row = current_cell // 9
            current_col = current_cell % 9

            # if before beginning of puzzle, unsolveable
            if current_cell < 0:
                print('UNSOLVABLE')
                self.unsolveable = True
                break

            # if we're moving backwards, go back until we hit a non-clue
            elif rewind:
                # if current index is a clue, keep going
                if self.index_was_given(current_row, current_col):
                    current_cell -= 1
                # if was not a clue, flip back rewind flag, start at next value for cell
                else:
                    rewind = False
                    current_value = self.puzzle[current_row, current_col] + 1
                    self.puzzle[current_row, current_col] = -1

            # if tried all values, try going back
            elif current_value > 9:
                # first set value to default
                self.puzzle[current_row, current_col] = -1
                # then move back cell counter until not a clue
                current_cell -= 1
                # reset current value and set rewind flag
                rewind = True

            # else try to solve it
            else:
                # if the current cell was a clue, move up blindly
                if self.index_was_given(current_row, current_col):
                    current_cell += 1
                # else try a number
                else:
                    # if current value works, assign and move up a cell
                    if self.index_can_have(current_row, current_col, current_value):
                        self.puzzle[current_row, current_col] = current_value
                        current_value = 1
                        current_cell += 1
                    # iterate current value if it didn't work
                    else:
                        current_value += 1

# make quick generator for making problems
def make_puzzle(num_clues: int) -> str:
    # used later for writing clues
    default_val = '.'
    possible_vals = np.array([1,2,3,4,5,6,7,8,9])
    cells_given = np.random.choice(81, num_clues, replace=False)
    # make empty string to hold puzzle
    puzzlestr = ""
    # loop through each cell and add clue or default value
    for idx in range(81):
        # add random value if given, default else
        if idx in cells_given:
            puzzlestr += str(np.random.choice(possible_vals))
        else:
            puzzlestr += default_val
    # return completed puzzle string
    return puzzlestr

# quick solution script to generate good sudoku problems and test solver
if __name__ == "__main__":
    # import solution checker
    from SolutionConsistencyChecker import SolutionConsistencyChecker
    import time

    # make some testing constants
    NUM_CLUES = 6
    NUM_PUZZLES = 1

    # make a wilkes solver and solution checker object
    solver = j_wilkes_b()
    solution_checker = SolutionConsistencyChecker(debug=True)

    # generate some puzzles
    problems = [make_puzzle(NUM_CLUES) for puzz in range(NUM_PUZZLES)]
    print(problems)

    # store variable for number of incorrectly solved puzzles
    incorrect_count = 0
    unsolveable_count = 0
    start_time = time.time()

    # loop through problems and (attempt) to solve
    for problem in problems:
        # initialize puzzle in solver
        solver.init_puzzle(problem)
        # solve puzzle using solver
        solver.solve_puzzle()
        # check solution correctness
        if not solution_checker.check_puzzle(solver.get_puzzle_string(), problem):
            incorrect_count += 1
        # check whether puzzle was unsolveable
        if solver.unsolveable:
            unsolveable_count += 1

    # store runtime stats
    solver_runtime = time.time() - start_time
    avg_solvetime = solver_runtime / len(problems)

    # store correctness stats
    percent_incorrect = float(incorrect_count) / len(problems)
    percent_unsolveable = float(unsolveable_count) / len(problems)

    # print statistics of solver
    print(f'\nStatistics of {solver} solver:')
    print(f'\ttime to solve {len(problems)} puzzles: {solver_runtime} seconds \n\t\t({avg_solvetime} sec/puzzle)')
    print(f'\tnumber of incorrect solutions: {incorrect_count} \n\t\t({percent_incorrect}%)')
    print(f'\tnumber of unsolveable problems: {unsolveable_count} \n\t\t({percent_unsolveable}%)')
