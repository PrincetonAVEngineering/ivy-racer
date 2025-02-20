import torch
from torchvision import models
import numpy as np

# Example: Load DeepLabv3 pretrained on COCO
model = models.segmentation.deeplabv3_resnet101(pretrained=True, num_classes=200)
model.eval()  # Set to evaluation mode

from torchvision.transforms import functional as F

# Load and preprocess an image
import cv2
image = cv2.imread("road.png")
cv2.imshow("Original Image", image)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Preprocessing
input_image = F.to_tensor(image)  # Convert to PyTorch Tensor
input_image = F.normalize(input_image, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
input_image = input_image.unsqueeze(0)  # Add batch dimension

# Perform inference
output = model(input_image)  # Access the segmentation output


segmentation_map = torch.argmax(output['out'].squeeze()[1:], dim=0).detach().cpu().numpy()

unique_values = np.unique(segmentation_map)
print("Unique segmentation values:", unique_values)

road_mask = (segmentation_map == 149)  # ROAD_CLASS_ID depends on the dataset/model
road_mask = road_mask.astype('uint8') * 255  # Convert to binary image

print(segmentation_map.shape)
print(segmentation_map)

for value in unique_values:
    cv2.imshow(f"Segmentation Map {value}", (segmentation_map == value).astype('uint8') * 255)
# cv2.imshow("segmentation_map", segmentation_map)
cv2.waitKey(0)

# overlay = cv2.addWeighted(image, 0.7, road_mask, 0.3, 0)
# cv2.imshow("Road Overlay", overlay)
# cv2.waitKey(0)