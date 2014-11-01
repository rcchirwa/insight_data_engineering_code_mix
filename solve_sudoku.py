#!/usr/bin/python

from sudoku_solver import *

import csv
import pandas as pd
import pickle
import sys


def main(argv):
    panda_frame = pd.read_csv(argv, header=None)

    sectors, columns, rows = get_grid_decomposiion_from_panda(panda_frame)

    potential_block_values, zero_coordinate_positions = \
        get_potential_block_values(panda_frame)
    values = permu(potential_block_values, [])

    correct = [1, 7, 9, 6, 5, 5, 1, 2, 6, 5, 5, 9, 7, 6, 1, 6,
               1, 8, 2, 3, 8, 6, 7, 1, 4, 3]

    flat_panda = flatten_panda_frame(panda_frame)

    missing_values, solutions = check_for_solutions(values,
                                                    zero_coordinate_positions,
                                                    flat_panda)

    solutions_in_rows_form = decompose_into_rows_from_list(solutions)
    write_to_solved_board_to_csv(solutions_in_rows_form, 'solved_puzzle.csv')


if __name__ == "__main__":
    main(sys.argv[1])
