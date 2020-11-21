from utils import *

row, col, matrix_dict = read_matrix('temp')

matrix_realize = {}
for name in matrix_dict.keys():
    content = int(name[1:])
    pos_list, sub_row, sub_col = matrix_dict[name]
    matrix_realize[name] = np.ones((sub_row, sub_col)) * content

## todo: turn a into a sparce matrix; readup on scipy.sparce.csc_matrix!!
A = realize_matrix(row, col, matrix_dict, matrix_realize)
print(A)
