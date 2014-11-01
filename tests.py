import sudoku_solver as solver
import unittest
import pandas as pd
import pickle
import os


class MyTest(unittest.TestCase):
    def setUp(self):
        self.panda_board = pd.read_csv('unsolved_puzzle.csv', header=None)
        self.flat_board = self.get_data_from_dat("board_as_series.dat")

    def get_data_from_dat(self, file_name):
        file_path = os.path.join('unitest_data', file_name)
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        return data

    def test_flatten_panda_frame(self):
        flat_data = solver.flatten_panda_frame(self.panda_board)
        test_data = self.get_data_from_dat("board_as_series.dat")

        self.assertEqual(len(flat_data), 81)
        self.assertEqual(flat_data, test_data)

    def test_decompose_into_blocks_from_panda(self):
        block_data = solver.decompose_into_blocks_from_panda(self.panda_board)
        test_data = self.get_data_from_dat("board_as_3x3_blocks.dat")
        self.assertEqual(block_data, test_data)

    def test_decompose_into_rows_from_panda(self):
        row_data = solver.decompose_into_rows_from_panda(self.panda_board)
        test_data = self.get_data_from_dat("board_as_rows.dat")
        self.assertEqual(row_data, test_data)

    def test_decompose_into_columns_from_panda(self):
        column_data = solver.decompose_into_columns_from_panda(
            self.panda_board)
        test_data = self.get_data_from_dat("board_as_columns.dat")
        self.assertEqual(column_data, test_data)

    def test_decompose_into_blocks_from_list(self):
        block_data = solver.decompose_into_blocks_from_list(self.flat_board)
        test_data = self.get_data_from_dat("board_as_3x3_blocks.dat")
        self.assertEqual(block_data, test_data)

    def test_decompose_into_rows_from_list(self):
        row_data = solver.decompose_into_rows_from_list(self.flat_board)
        test_data = self.get_data_from_dat("board_as_rows.dat")
        self.assertEqual(row_data, test_data)

    def test_decompose_into_columns_from_list(self):
        column_data = solver.decompose_into_columns_from_list(self.flat_board)
        test_data = self.get_data_from_dat("board_as_columns.dat")
        self.assertEqual(column_data, test_data)

    def test_get_grid_decomposiion_from_panda(self):
        test_sectors = self.get_data_from_dat("board_as_3x3_blocks.dat")
        test_columns = self.get_data_from_dat("board_as_columns.dat")
        test_rows = self.get_data_from_dat("board_as_rows.dat")
        sectors, columns, rows = solver.get_grid_decomposiion_from_panda(
            self.panda_board)
        self.assertEqual(sectors, test_sectors)
        self.assertEqual(columns, test_columns)
        self.assertEqual(rows, test_rows)

    def test_get_grid_decomposiion_from_list(self):
        test_sectors = self.get_data_from_dat("board_as_3x3_blocks.dat")
        test_columns = self.get_data_from_dat("board_as_columns.dat")
        test_rows = self.get_data_from_dat("board_as_rows.dat")
        sectors, columns, rows = \
            solver.get_grid_decomposiion_from_list(self.flat_board)

    def test_get_potential_block_values(self):
        data_file = "potential_space_values.dat"
        test_potential_solutions = self.get_data_from_dat(data_file)
        data_file = "blank_space_coordinates.dat"
        test_zero_coordinate_position = self.get_data_from_dat(data_file)
        potential_solutions, zero_coordinate_positions = \
            solver.get_potential_block_values(self.panda_board)
        self.assertEqual(potential_solutions,
                         test_potential_solutions)
        self.assertEqual(zero_coordinate_positions,
                         test_zero_coordinate_position)

    def test_permu(self):
        data = [['a', 'b', 'c'], [1], ['one', 'two']]
        expected_data = [['a', 1, 'one'], ['a', 1, 'two'], ['b', 1, 'one'],
                         ['b', 1, 'two'], ['c', 1, 'one'], ['c', 1, 'two']]
        permutations = solver.permu(data)
        self.assertEqual(permutations, expected_data)

    def test_permu_base_case(self):
        data = [['one']]
        expected_data = [['one']]
        permutations = solver.permu(data)
        self.assertEqual(permutations, expected_data)

    def test_permu_on_board_data(self):
        data_file = "potential_solutions.dat"
        test_potential_solutions = self.get_data_from_dat(data_file)
        data_file = "potential_space_values.dat"
        cached_potential_block_values = self.get_data_from_dat(data_file)
        potential_solutions = solver.permu(cached_potential_block_values)
        self.assertEqual(potential_solutions, test_potential_solutions)

    def test_check_for_valid_combos(self):
        valid_combo_1 = [range(1, 10)]
        valid_combo_2 = [[3, 6, 9, 1, 4, 7, 2, 5, 8]]
        valid_combo_3 = valid_combo_1 + valid_combo_2

        invalid_combo_1 = [range(9)]
        invalid_combo_2 = [range(8, 17)]
        invalid_combo_3 = [[1, 2, 3, 3, 5, 6, 7, 8, 9]]
        invalid_combo_4 = [range(10)]
        invalid_combo_5 = valid_combo_3 + invalid_combo_1

        valid_result_1 = solver.check_for_valid_combos(valid_combo_1)
        valid_result_2 = solver.check_for_valid_combos(valid_combo_2)
        valid_result_3 = solver.check_for_valid_combos(valid_combo_3)

        invalid_result_1 = solver.check_for_valid_combos(invalid_combo_1)
        invalid_result_2 = solver.check_for_valid_combos(invalid_combo_2)
        invalid_result_3 = solver.check_for_valid_combos(invalid_combo_3)
        invalid_result_4 = solver.check_for_valid_combos(invalid_combo_4)
        invalid_result_5 = solver.check_for_valid_combos(invalid_combo_5)

        self.assertTrue(valid_result_1)
        self.assertTrue(valid_result_2)
        self.assertTrue(valid_result_3)

        self.assertFalse(invalid_result_1)
        self.assertFalse(invalid_result_2)
        self.assertFalse(invalid_result_3)
        self.assertFalse(invalid_result_4)
        self.assertFalse(invalid_result_5)

    def test_check_for_solutions(self):
        flat_board = self.flat_board
        potential_solutions = self.get_data_from_dat("potential_solutions.dat")
        data_file = "blank_space_coordinates.dat"
        zero_coordinate_positions = self.get_data_from_dat(data_file)

        data_file = "solution_missing_values.dat"
        test_solution = self.get_data_from_dat(data_file)

        data_file = "flat_solution_board.dat"
        test_completed_board = self.get_data_from_dat(data_file)

        solution, completed_board = \
            solver.check_for_solutions(potential_solutions,
                                       zero_coordinate_positions,
                                       flat_board)

        self.assertEqual(solution, test_solution)
        self.assertEqual(completed_board, test_completed_board)

    def test_get_positional_values_from_index(self):
        short_alias = solver.get_positional_values_from_index
        self.assertEqual(short_alias(0), (0, 0, 0, 0, 0))
        self.assertEqual(short_alias(9), (0, 1, 0, 0, 0))
        self.assertEqual(short_alias(23), (5, 2, 0, 1, 1))
        self.assertEqual(short_alias(35), (8, 3, 1, 2, 5))
        self.assertEqual(short_alias(45), (0, 5, 1, 0, 3))
        self.assertEqual(short_alias(48), (3, 5, 1, 1, 4))
        self.assertEqual(short_alias(55), (1, 6, 2, 0, 6))
        self.assertEqual(short_alias(61), (7, 6, 2, 2, 8))

if __name__ == '__main__':
    unittest.main()
