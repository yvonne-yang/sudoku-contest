from Yvonne import Yvonne
from noor import noor
from ollybritton import ollybritton
from saf import saf
from Jeison import Jeison
from j_wilkes_b import j_wilkes_b
from Khaled import Khaled
from Aditya import Aditya

if __name__ == "__main__":
    ##
    #   Load sudoku puzzles however you want here into a list of strings called "problems"
    ##

    ##
    #   Load sudoku solutions however you want here into a list of strings called "solutions"
    ##

    # store total number of puzzles
    total_puzzles = len(problems)

    solvers = [
            Yvonne(),
            noor(),
            ollybritton(),
            saf(),
            Jeison(),
            j_wilkes_b(),
            Khaled(),
            Aditya()
            ]

    # loop through all puzzles with all solvers and print statistics
    for solver in solvers:
        # store variable for number of incorrectly solved puzzles
        incorrect_count = 0
        for problem, solution in zip(problems, solutions):
            # initialize puzzle in solver
            solver.init_puzzle(problem)
            # solve puzzle using solver
            solver.solve_puzzle()
            # check solution correctness
            if solution != solver.get_puzzle_string():
                incorrect_count += 1
        # store runtime stats
        solver_runtime = time.time() - start_time
        avg_solvetime = solver_runtime / float(total_puzzles)
        # store correctness stats
        percent_incorrect = float(incorrect_count) / float(total_puzzles)
        # print statistics of solver
        print(f'\nStatistics of {solver} solver:')
        print(f'\ttime to solve {total_puzzles} puzzles: {solver_runtime} seconds \n\t\t({avg_solvetime} sec/puzzle)')
        print(f'\tnumber of incorrect solutions: {incorrect_count} \n\t\t({percent_incorrect}%)')

