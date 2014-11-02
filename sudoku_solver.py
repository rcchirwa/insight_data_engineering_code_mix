import csv
import pickle
import copy


def get_board_as_rows(file_name):
    board_as_rows = []
    with open(file_name) as csv_file:
        csvreader = csv.reader(csv_file)
        for row in csvreader:
            row = map(lambda x: int(x), row)
            board_as_rows.append(row)
    return board_as_rows


def write_to_solved_board_to_csv(solution, file_name):
    with open(file_name, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(solution)


def flatten_extracted_rows(rows):
    linear_repr = []
    for row in rows:
        linear_repr = linear_repr + row
    return linear_repr


def decompose_into_blocks_from_rows(board_as_rows):
    flattened_frame = []
    flattened_frame = flatten_extracted_rows(board_as_rows)
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


def decompose_into_rows_from_list(list_in):
    rows = []
    for x in range(9):
        initial_position = x*9
        rows.append(list_in[initial_position:initial_position+9])
    return rows


def decompose_into_columns_from_rows(rows):
    columns = []
    flat_board = flatten_extracted_rows(rows)
    columns = decompose_into_columns_from_list(flat_board)
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


def get_grid_decomposiion_from_rows(rows):
    sectors = decompose_into_blocks_from_rows(rows)
    columns = decompose_into_columns_from_rows(rows)
    return sectors, columns, rows


def get_grid_decomposiion_from_list(list_in):
    sectors = decompose_into_blocks_from_list(list_in)
    columns = decompose_into_columns_from_list(list_in)
    rows = decompose_into_rows_from_list(list_in)
    return sectors, columns, rows


def get_positional_values_from_index(index):
    column = index % 9
    row = index/9
    sector_row = index/27
    sector_column = column/3
    sector_postion = 3*sector_row + sector_column

    return column, row, sector_row, sector_column, sector_postion


def get_potential_block_values(flat_board):

    sectors, columns, rows = get_grid_decomposiion_from_list(flat_board)

    STATIC_SET = set(range(1, 10))

    potential_block_values = []
    zero_coordinate_positions = []

    for i, val in enumerate(flat_board):
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


# TO-DO: permu should be generator so it could
# genearate and check so break after first solution is found
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
                        zero_coordinate_positions, flat_board):
    for i, solution in enumerate(potential_solutions):
        for index, position in enumerate(zero_coordinate_positions):
            flat_board[position] = solution[index]

        sectors_popultaed = decompose_into_blocks_from_list(flat_board)
        columns_populated = decompose_into_columns_from_list(flat_board)
        rows_populated = decompose_into_rows_from_list(flat_board)

        if not (check_for_valid_combos(sectors_popultaed) or
                check_for_valid_combos(rows_populated) or
                check_for_valid_combos(columns_populated)):
            continue

        return solution, flat_board
