import numpy as np


def output_example(matrix_dict):
	result = np.zeros((20, 20))

	result[7:10, 8:10] = matrix_dict['Sparse'].T
	result[6:8, 6:9] = matrix_dict['Sparse']
	result[15:16, 9:12] = -1 * matrix_dict['dense']
	result[4:6, 3:5] = matrix_dict['Yay']

	return result
