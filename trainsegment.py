import numpy as np
import matplotlib.pyplot as plt
import cv2 
import torch
import torchvision
import sys
sys.path.append("..")

from segment_anything import sam_model_registry, SamPredictor


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    


# device config for running sam 
sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "mps"

# image margin for point
BOTTOM_MARGIN = 500

# model set up
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

'''
# set up predictor
predictor = SamPredictor(sam)
predictor.set_image(image)
'''


def get_masked_frame(image):
    #image set up
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape  # (rows, cols)

    # feed in prompt point into model
    input_point = np.array([[image_width // 2, image_height - BOTTOM_MARGIN]])
    input_label = np.array([1])

    # Draw the point as a small circle
    cv2.circle(image, input_point[0], radius=5, color=(0, 255, 0), thickness=-1)

    return image
    






'''

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True, # prints best mask (False) or three masks(True)
)

masks.shape  # (number_of_masks) x H x W
best_mask, best_score = sorted(zip(masks, scores), key=lambda x: x[1], reverse=True)[0]

plt.figure(figsize=(10,10))
plt.imshow(image)
show_mask(best_mask, plt.gca())
show_points(input_point, input_label, plt.gca())
plt.title(f"Best Mask, Score: {best_score:.3f}", fontsize=18)
plt.axis('off')
plt.show()  


for i, (mask, score) in enumerate(zip(masks, scores)):
    plt.figure(figsize=(10,10))
    plt.imshow(image)
    show_mask(mask, plt.gca())
    show_points(input_point, input_label, plt.gca())
    plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
    plt.axis('off')
    plt.show()  
  '''
#print(mask)
#print(type(mask)) 

# convert bool mask to bin nums
# mask = mask.astype(np.uint8)




#np.set_printoptions(threshold=np.inf)  
#print(mask)

#blank = np.zeros(image.shape, dtype='uint8')
#cv2.imshow('Blank', blank)

#ret, thres = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY)
#cv2.imshow('Threshold', thres)

#contours, hierarchies = cv2.findContours(thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#print(f'{len(contours)} contour(s) found!')

#cv2.drawContours(blank, contours, -1, (0,0,255), 1)
#cv2.imshow('Contours Drawn', blank)