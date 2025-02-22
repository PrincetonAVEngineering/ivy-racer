# Important stuff

## Idea on how to create more accurate segmentation:

- Get a first calibration mask from the road currently.
- For the next mask, choose multiple points within the road and then morph them into one mask.
- Use YOLO to avoid picking points within
