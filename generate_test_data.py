from sudoku_solver import *

import csv
import pickle
import os.path

row_form_board = get_board_as_rows('unsolved_puzzle.csv')

sectors, columns, rows = get_grid_decomposiion_from_rows(
    row_form_board)

flat_solution_board = flatten_extracted_rows(row_form_board)

potential_block_values, zero_coordinate_positions = \
    get_potential_block_values(flat_solution_board)

values = permu(potential_block_values, [])

solution, final_matrix = check_for_solutions(values,
                                             zero_coordinate_positions,
                                             flat_solution_board)


def stash_data(PIK, data):
    file_path = os.path.join('unitest_data', PIK)
    with open(file_path, "w+") as f:
        pickle.dump(data, f)


print "Strarting to Generate test data"

PIK = "board_as_series.dat"
data = flatten_extracted_rows(row_form_board)
stash_data(PIK, data)

PIK = "board_as_3x3_blocks.dat"
data = sectors
stash_data(PIK, data)

PIK = "board_as_rows.dat"
data = rows
stash_data(PIK, data)

PIK = "board_as_columns.dat"
data = columns
stash_data(PIK, data)

PIK = "potential_space_values.dat"
data = potential_block_values
stash_data(PIK, data)

PIK = "blank_space_coordinates.dat"
data = zero_coordinate_positions
stash_data(PIK, data)

PIK = "potential_solutions.dat"
data = values
stash_data(PIK, data)

PIK = "solution_missing_values.dat"
data = solution
stash_data(PIK, data)

PIK = "flat_solution_board.dat"
data = final_matrix
stash_data(PIK, data)

print "Finished Generating Test Data"
