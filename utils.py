import numpy as np
from scipy import sparse

"""
NOTE
Format of the savings
NAME X_POS Y_POS HEIGHT(row) WIDTH(col)
"""


def realize_numpy_matrix(file_name, matrix_dict):
    result_matrix = None

    with open(f'Saved_Matrix/{file_name}.txt', 'r') as f:
        rows, cols = f.readline().split()
        result_matrix = np.zeros((int(rows), int(cols)))

        f_line = f.readline()
        while len(f_line) > 0:
            name, pos_x, pos_y, sub_row, sub_col = f_line.split()
            pos_x = int(pos_x)
            pos_y = int(pos_y)
            sub_row = int(sub_row)
            sub_col = int(sub_col)
            name_index = name
            if name[0] == '-':
                name_index = name_index[1:]
            if name[-2:] == '.T':
                name_index = name_index[:-2]
            sub_matrix = matrix_dict[name_index].copy()
            if name[0] == '-':
                sub_matrix *= -1
            if name[-2:] == '.T':
                sub_matrix = sub_matrix.T

            result_matrix[pos_y:pos_y+sub_row, pos_x:pos_x + sub_col] = sub_matrix
            f_line = f.readline()

    return result_matrix


def realize_coo_matrix(file_name, matrix_dict):
    result_matrix = None

    with open(f'Saved_Matrix/{file_name}.txt', 'r') as f:
        rows, cols = f.readline().split()
        rows = int(rows)
        cols = int(cols)

        row_index = list()
        col_index = list()
        values = list()

        f_line = f.readline()
        while len(f_line) > 0:
            name, pos_x, pos_y, sub_row, sub_col = f_line.split()
            pos_x = int(pos_x)
            pos_y = int(pos_y)
            sub_row = int(sub_row)
            sub_col = int(sub_col)
            name_index = name
            if name[0] == '-':
                name_index = name_index[1:]
            if name[-2:] == '.T':
                name_index = name_index[:-2]
            sub_matrix = matrix_dict[name_index].copy()
            if name[0] == '-':
                sub_matrix *= -1
            if name[-2:] == '.T':
                sub_matrix = sub_matrix.T

            for r in range(len(sub_matrix)):
                for c in range(len(sub_matrix[0])):
                    row_index.append(pos_y + r)
                    col_index.append(pos_x + c)
                    values.append(sub_matrix[r, c])

            f_line = f.readline()

        result_matrix = sparse.coo_matrix((np.array(values), (np.array(row_index), np.array(col_index))), shape=(rows, cols))

    return result_matrix


def sparse_matrix(matrix):
    return sparse.csr_matrix(matrix)




