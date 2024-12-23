import numpy as np


def swap_input(matrix:np.array, input_vector, initial_row, final_row, reference_vector=None):
    matrix[:, [initial_row, final_row]] = matrix[:, [final_row, initial_row]]
    input_vector[[initial_row, final_row]] = input_vector[[final_row, initial_row]]
    if reference_vector is not None:
        reference_vector[[initial_row, final_row]] = reference_vector[[final_row, initial_row]]

def swap_output(matrix:np.array, output_vector, initial_row, final_row, reference_vector=None):
    matrix[[initial_row, final_row]] = matrix[[final_row, initial_row]]
    output_vector[[initial_row, final_row]] = output_vector[[final_row, initial_row]]
    if reference_vector is not None:
        reference_vector[[initial_row, final_row]] = reference_vector[[final_row, initial_row]]

def swap_full(matrix:np.array, input_vector, output_vector, initial_row, final_row, reference_vector=None):
    swap_input(matrix, input_vector, initial_row, final_row, reference_vector)
    swap_output(matrix, output_vector, initial_row, final_row, reference_vector)

if __name__ == "__main__":

    vector = np.array([1, 2, 3])
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # print(np.matvec(matrix[[1,2,0]], vector[[1,2,0]]))
    # print(matrix[[1,2,0]])
    print(matrix)
    print(vector)
    print("Output", np.matvec(matrix, vector))

    swap_input(matrix, vector, 0, 2)
    output_vector = np.array([14, 32, 50])
    print(matrix)
    print(vector)
    print("Output", np.matvec(matrix, vector))

    swap_output(matrix, output_vector, 0, 2)
    print(matrix)
    print(output_vector)
    print("Output", np.matvec(matrix, vector))