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
print(sparse_matrix(A))

"""
def matrix_func(matrix_dict):
	result = np.zeros((20, 10))

	result[0:2,0:2] = matrix_dict['M0']
	result[2:6,2:6] = matrix_dict['M1']
	result[14:16,1:3] = matrix_dict['M2']
	result[16:18,8:10] = matrix_dict['M3']
	result[7:9,6:8] = matrix_dict['M4']

	return result
"""


temp = dict()
temp['M0'] = 10 * np.ones((2, 2))
temp['M1'] = 11 * np.ones((4, 4))
temp['M2'] = 20 * np.ones((2, 2))
temp['M3'] = 30 * np.ones((2, 2))
temp['M4'] = 40 * np.ones((2, 2))
A = matrix_func(temp)
print(A)

