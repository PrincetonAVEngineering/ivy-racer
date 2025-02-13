import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_average_index_high(image, row=0):
    indices = np.where(image[row] == 1)
    if len(indices) == 0:
        return None
    median_index = np.median(indices)
    return median_index

#loop through all rows, create list of medians, plot point on image for each median to create path

test = np.array([[0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]])

#print(get_average_index_high(test))

image = cv2.imread('Images/segmentation_mask_3.png', cv2.IMREAD_GRAYSCALE)
_, mask = cv2.threshold(image, 127, 1, cv2.THRESH_BINARY)

# Display the mask
plt.imshow(mask, cmap="gray")
plt.title("Binary Mask")
plt.show()

print(mask)

#print(np.where(image == 1))

print(get_average_index_high(mask,3000))