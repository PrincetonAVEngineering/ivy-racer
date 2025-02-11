import numpy as np

def get_average_index_high(image, row=0):
    indices = np.where(image[row] == 1)
    if len(indices) == 0:
        return None
    median_index = np.median(indices)
    return median_index

test = np.array([[0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]])

print(get_average_index_high(test))