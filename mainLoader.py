from utils import *


# Example 1
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
print(sparse_matrix(A))


# Example 2
B = realize_numpy_matrix('second', temp)
print(B)
#print(realize_coo_matrix('second', temp))

# Example 3
import numpy as np
from scipy import sparse

def presentation(matrix_dict):
	row_indices = list()
	col_indices = list()
	values = list()
	row_indices.append(0)
	col_indices.append(0)
	values.append(matrix_dict['M1'][0, 0])

	row_indices.append(1)
	col_indices.append(0)
	values.append(matrix_dict['M1'][1, 0])

	row_indices.append(2)
	col_indices.append(0)
	values.append(matrix_dict['M1'][2, 0])

	row_indices.append(5)
	col_indices.append(0)
	values.append(matrix_dict['M4'][0, 0])

	row_indices.append(5)
	col_indices.append(1)
	values.append(matrix_dict['M4'][0, 1])

	row_indices.append(6)
	col_indices.append(0)
	values.append(matrix_dict['M4'][1, 0])

	row_indices.append(6)
	col_indices.append(1)
	values.append(matrix_dict['M4'][1, 1])

	row_indices.append(10)
	col_indices.append(5)
	values.append(-1 * matrix_dict['testing'][0, 0])

	row_indices.append(10)
	col_indices.append(6)
	values.append(-1 * matrix_dict['testing'][1, 0])

	row_indices.append(11)
	col_indices.append(5)
	values.append(-1 * matrix_dict['testing'][0, 1])

	row_indices.append(11)
	col_indices.append(6)
	values.append(-1 * matrix_dict['testing'][1, 1])

	row_indices.append(12)
	col_indices.append(5)
	values.append(-1 * matrix_dict['testing'][0, 2])

	row_indices.append(12)
	col_indices.append(6)
	values.append(-1 * matrix_dict['testing'][1, 2])

	row_indices.append(9)
	col_indices.append(1)
	values.append(matrix_dict['M3'][0, 0])

	row_indices.append(10)
	col_indices.append(1)
	values.append(matrix_dict['M3'][0, 1])

	row_indices.append(11)
	col_indices.append(1)
	values.append(matrix_dict['M3'][0, 2])

	row_indices.append(3)
	col_indices.append(4)
	values.append(-1 * matrix_dict['M5'][0, 0])

	row_indices.append(3)
	col_indices.append(5)
	values.append(-1 * matrix_dict['M5'][0, 1])

	row_indices.append(3)
	col_indices.append(6)
	values.append(-1 * matrix_dict['M5'][0, 2])

	row_indices.append(3)
	col_indices.append(1)
	values.append(-1 * matrix_dict['M0'][0, 0])

	row_indices.append(3)
	col_indices.append(2)
	values.append(-1 * matrix_dict['M0'][1, 0])

	row_indices.append(4)
	col_indices.append(1)
	values.append(-1 * matrix_dict['M0'][0, 1])

	row_indices.append(4)
	col_indices.append(2)
	values.append(-1 * matrix_dict['M0'][1, 1])

	return sparse.coo_matrix((np.array(values), (np.array(row_indices), np.array(col_indices))), shape=(13, 7))



C = presentation(temp)
print(C)

