import numpy as np


"""
NOTE
Format of the savings
NAME Y_POS X_POS HEIGHT(row) WIDTH(col)
"""


def read_matrix(file_name):
    matrix_dict = dict()
    row = 0
    col = 0

    with open(f'Saved_Matrix/{file_name}.txt', 'r') as f:
        row, col = f.readline().split()

        f_line = f.readline()
        while len(f_line) > 0:
            name, pos_row, pos_col, sub_row, sub_col = f_line.split()
            pos = (int(pos_row), int(pos_col))
            if name in matrix_dict.keys():
                matrix_dict[name][0].append(pos)
            else:
                matrix_dict[name] = ([pos], int(sub_row), int(sub_col))
            f_line = f.readline()

    return int(row), int(col), matrix_dict


def realize_matrix(row, col, matrix_dict, matrix_realize_dict):
    result_matrix = np.zeros((row, col))

    for name in matrix_realize_dict.keys():
        sub_matrix = np.array(matrix_realize_dict[name])
        pos_list, sub_row, sub_col = matrix_dict[name]

        for pos in pos_list:
            pos_row, pos_col = pos
            result_matrix[pos_row:(pos_row + sub_row), pos_col:(pos_col + sub_col)] = sub_matrix

    return result_matrix
