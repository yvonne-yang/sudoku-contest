# sudoku-contest
A friendly contest for people in the AIMA reading group. Try not to cheat as the goal is to explore and learn different strategies to solve constraint satisfaction problems. 

Potential benchmarks:
https://github.com/t-dillon/tdoku/tree/master/benchmarks

Typical input files have multiple puzzles, each on a separate line like so:  
`4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......`  
This particular line represents the puzzle below:  
```
4 . . |. . . |8 . 5 
. 3 . |. . . |. . . 
. . . |7 . . |. . . 
------+------+------
. 2 . |. . . |. 6 . 
. . . |. 8 . |4 . . 
. . . |. 1 . |. . . 
------+------+------
. . . |6 . 3 |. 7 . 
5 . . |2 . . |. . . 
1 . 4 |. . . |. . . 
```
The output file from your solver should have the same format, except that all blank spaces should be filled (no `.`s).

# Rules
(TBD)
We will most likely constrain the programming language to be Python.
