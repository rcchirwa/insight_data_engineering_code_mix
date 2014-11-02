#!/usr/bin/python

from sudoku_solver import *

import csv
import pickle
import sys


def main(argv):

    print "Initializing Unsolved Puzzle......"
    row_form_board = get_board_as_rows(argv)

    print "Transforming puzzle into 3_x_3, Row and Column projections.... "
    sectors, columns, rows = get_grid_decomposiion_from_rows(
        row_form_board)

    print "Creating flat versions of puzzle...."
    flat_panda = flatten_extracted_rows(row_form_board)

    print "Get potential soltion block values..."
    potential_block_values, zero_coordinate_positions = \
        get_potential_block_values(flat_panda)

    # TO DO permu should be generator so it could
    # genearate and check so break after first solution is found
    print "generate all potential combination of solutions........"
    values = permu(potential_block_values, [])

    print "Search all possible solutions for correct one"
    missing_values, solutions = check_for_solutions(values,
                                                    zero_coordinate_positions,
                                                    flat_panda)

    print "Convert the soltion back into rows"
    solutions_in_rows_form = decompose_into_rows_from_list(solutions)

    print "Outputing solution to 'solved_puzzle.csv'"
    write_to_solved_board_to_csv(solutions_in_rows_form, 'solved_puzzle.csv')

    print "Solved: Enjoy reviewing your Solution"
if __name__ == "__main__":
    main(sys.argv[1])
