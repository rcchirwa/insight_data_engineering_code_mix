#Insight Data Engineering Code Challenge

####*Mashed Up in Python*

A Sudoku Puzzle Solver mixed in Python 2.7.8. The goal of the project is to produce a board with a correct solution as long as the given board is valid. 

####Running the Puzzle Solver:

The only non-standard python library that is needed to run this program is the popular pandas library utilized for data analysis.

The program can be executed as follows using the sample file, unsolved_puzzle.csv, contained in the repository:

`$ python solve_sudoku.py unsolved_puzzle.csv`

If you wish to solve another puzzle , simply, as in the above example replace unsolved_puzzle.csv with the name of the file containing your puzzle as follows:

`$ python solve_sudoku.py [file name of csv containing your puzzle]`

The correct board is output to the file called solved_puzzle.csv. This file is output to the same directory containing solve_sudoku.py

####Working with the Unit Tests:


Unit Tests have been added for potential regression testing purposes. The only non-standard library that might be required for to run the tests is the mock library used to mock during unit testing.

The tests can be run from the command lines as follows: 

`$ python tests.py -v`

The output will tell you if the tests are still valid after potential refactoring or code changes. 

Test data has already been generated and included in the the following folder:
unitest_data

The data was populated in the unitest_data directory by running the following command which uses the included unsolved_puzzle.csv example to regenerate the test data:

`python generate_test_data.py`

