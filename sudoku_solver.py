import csv
import pandas as pd
import pickle
import copy


def flatten_panda_frame(panda_frame):
    linear_repr = []
    for x in range(len(panda_frame)):
        linear_repr = linear_repr + list(panda_frame.iloc[x].values)
    return linear_repr


def decompose_into_blocks_from_panda(panda_frame):
    flattened_frame = []
    flattened_frame = flatten_panda_frame(panda_frame)
    decomposed = decompose_into_blocks_from_list(flattened_frame)
    return decomposed


def decompose_into_blocks_from_list(list_1D):
    decomposed_blocks = []
    # jump 27 to start harvestiong next sequencue
    # 27 contiguous values represents a cluster of
    # 3 3x3 blocks
    for three_block_group in range(3):
        # perform a shift of three to get the start point of
        # data from block to be extracted
        for block_start in range(3):
            extracted_block = []
            # get jump 9 from previous start to find next set of
            # values associated with ROW OF BLOCK being harvets
            for block_row in range(3):
                # get three adjacent values block row
                for block_values in range(3):
                    block_index = block_values + (block_row*9) + (block_start*3) + \
                        (three_block_group * 27)

                    block_value = list_1D[block_index]
                    extracted_block.append(block_value)

            decomposed_blocks.append(extracted_block)
    return decomposed_blocks


def decompose_into_rows_from_panda(panda_frame):
    rows = []
    for x in range(len(panda_frame)):
        rows.append(list(panda_frame.iloc[x].values))
    return rows


def decompose_into_rows_from_list(list_in):
    rows = []
    for x in range(9):
        initial_position = x*9
        rows.append(list_in[initial_position:initial_position+9])
    return rows


def decompose_into_columns_from_panda(panda_frame):
    columns = []
    for x in range(len(panda_frame)):
        columns.append(list((panda_frame[x].values)))
    return columns


def decompose_into_columns_from_list(list_in):
    rows = []
    for a in range(9):
        row = []
        for i in range(a, 81, 9):
            value = list_in[i]
            row.append(value)
        rows.append(row)
    return rows


def get_grid_decomposiion_from_panda(panda_frame):
    sectors = decompose_into_blocks_from_panda(panda_frame)
    columns = decompose_into_columns_from_panda(panda_frame)
    rows = decompose_into_rows_from_panda(panda_frame)
    return sectors, columns, rows


def get_grid_decomposiion_from_list(list_in):
    sectors = decompose_into_blocks_from_list(list_in)
    columns = decompose_into_columns_from_list(list_in)
    rows = decompose_into_rows_from_list(list_in)
    return sectors, columns, rows


# TO do write test
def get_positional_values_from_index(index):
    column = index % 9
    row = index/9
    sector_row = index/27
    sector_column = column/3
    sector_postion = 3*sector_row + sector_column

    return column, row, sector_row, sector_column, sector_postion


def get_potential_block_values(panda_frame):

    sectors, columns, rows = get_grid_decomposiion_from_panda(panda_frame)

    flat_panda = flatten_panda_frame(panda_frame)
    STATIC_SET = set(range(1, 10))

    potential_block_values = []
    zero_coordinate_positions = []

    for i, val in enumerate(flat_panda):
        if val == 0:
            column, row, sector_row, sector_column, sector_postion = \
                get_positional_values_from_index(i)

            sects = sectors[sector_postion]
            rws = rows[row]
            cols = columns[column]

            all_values = sects + rws + cols
            unique_value = set(all_values)
            unique_value.remove(0)

            candidates = STATIC_SET.difference(unique_value)

            zero_coordinate_positions.append(i)
            potential_block_values.append(list(candidates))

    return potential_block_values, zero_coordinate_positions


def permu(list_values, path=list()):
    combos = []
    start_index = 0

    for potential_solution in list_values[start_index]:
        temp_path = copy.deepcopy(path)
        temp_path.append(potential_solution)
        # base case is last value reached
        if len(list_values) == 1:
            combos.append(temp_path)
        elif temp_path != path:
            pathsearch = permu(list_values[start_index + 1:], temp_path)
            if pathsearch:
                for p in pathsearch:
                    combos.append(p)
    return combos


def check_for_valid_combos(combos):
    reference = set(range(1, 10))
    for combo in combos:
        if reference != set(combo):
            return False
    return True


def check_for_solutions(potential_solutions,
                        zero_coordinate_positions, flat_panda):
    for i, solution in enumerate(potential_solutions):
        for index, position in enumerate(zero_coordinate_positions):
            flat_panda[position] = solution[index]

        sectors_popultaed = decompose_into_blocks_from_list(flat_panda)
        columns_populated = decompose_into_columns_from_list(flat_panda)
        rows_populated = decompose_into_rows_from_list(flat_panda)

        if not (check_for_valid_combos(sectors_popultaed) or
                check_for_valid_combos(rows_populated) or
                check_for_valid_combos(columns_populated)):
            continue

        return solution, flat_panda


def write_to_solved_board_to_csv(solution, file_name):
    with open(file_name, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(solution)
