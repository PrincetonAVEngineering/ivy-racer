from tensorflow.keras.models import load_model
from tensorflow import expand_dims, squeeze
from tensorflow.image import sobel_edges
import cv2
import numpy as np
import tensorflow.keras.layers as lay

class Sobel(lay.Layer):
    def call(self, x):
        return sobel_edges(x)[:,:,:,:,0] + sobel_edges(x)[:,:,:,:,1]

model = load_model("clarity(most_trained).keras", custom_objects={'Sobel': Sobel})

# Open the default camera
cam = cv2.VideoCapture("road2.mp4")
# cam = cv2.VideoCapture(0)

def make_3d(input):
    return np.stack((input, input, input), axis=-1)

while True:
    ret, frame = cam.read()
    if not ret:
        break
        
    frame_resized = cv2.resize(frame, (512,512)) / 255.0
    
    result = model(expand_dims(frame_resized, 0))
    result = squeeze(result)
    result = make_3d(result)
    shown = np.concatenate((result, frame_resized), axis=1)

    cv2.imshow('Outputs', shown)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cam.release()
cv2.destroyAllWindows()