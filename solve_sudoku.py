#!/usr/bin/python

from sudoku_solver import *

import csv
import pickle
import sys

import pandas as pd


def main(argv):

    row_form_board = get_board_as_rows(argv)

    sectors, columns, rows = get_grid_decomposiion_from_rows(
        row_form_board)

    flat_panda = flatten_extracted_rows(row_form_board)

    potential_block_values, zero_coordinate_positions = \
        get_potential_block_values(flat_panda)

    # TO DO permu should be generator so it could
    # genearate and check so break after first solution is found
    values = permu(potential_block_values, [])

    correct = [1, 7, 9, 6, 5, 5, 1, 2, 6, 5, 5, 9, 7, 6, 1, 6,
               1, 8, 2, 3, 8, 6, 7, 1, 4, 3]

    missing_values, solutions = check_for_solutions(values,
                                                    zero_coordinate_positions,
                                                    flat_panda)

    solutions_in_rows_form = decompose_into_rows_from_list(solutions)
    write_to_solved_board_to_csv(solutions_in_rows_form, 'solved_puzzle.csv')

if __name__ == "__main__":
    main(sys.argv[1])
