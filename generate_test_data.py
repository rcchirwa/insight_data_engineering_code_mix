from sudoku_solver import *

import csv
import pandas as pd
import pickle

panda_frame = pd.read_csv('unsolved_puzzle.csv', header=None)

sectors, columns, rows = get_grid_decomposiion_from_panda(panda_frame)

potential_block_values, zero_coordinate_positions = \
    get_potential_block_values(panda_frame)
values = permu(potential_block_values, [])

correct = [1, 7, 9, 6, 5, 5, 1, 2, 6, 5, 5, 9, 7,
           6, 1, 6, 1, 8, 2, 3, 8, 6, 7, 1, 4, 3]

flat_panda = flatten_panda_frame(panda_frame)

solution, final_matrix = check_for_solutions(values,
                                             zero_coordinate_positions,
                                             flat_panda)

import os.path


def stash_data(PIK, data):
    file_path = os.path.join('unitest_data', PIK)
    with open(file_path, "w+") as f:
        pickle.dump(data, f)

PIK = "board_as_series.dat"
data = flatten_panda_frame(panda_frame)
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

print solution == correct
