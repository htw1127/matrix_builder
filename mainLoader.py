from utils import *

# Example 1
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

# Example 2
def matrix_func(matrix_dict):
	result = np.zeros((13, 7))

	result[0:3, 0:1] = matrix_dict['M1']
	result[5:7, 0:2] = matrix_dict['M4']
	result[10:13, 5:7] = -1 * matrix_dict['testing'].T
	result[9:12, 1:2] = matrix_dict['M3'].T
	result[3:4, 4:7] = -1 * matrix_dict['M5']
	result[3:5, 1:3] = -1 * matrix_dict['M0'].T

	return result






temp = dict()
temp['M0'] = 10 * np.ones((2, 2))
temp['M1'] = 11 * np.ones((3, 1))
temp['M3'] = np.array([[1, 2, 3]])
temp['M4'] = 44 * np.ones((2, 2))
temp['M5'] = 55 * np.ones((1, 3))
temp['testing'] = np.arange(6).reshape((2, 3))
A = matrix_func(temp)
print(A)

