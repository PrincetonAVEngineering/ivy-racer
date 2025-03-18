import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model("lane_detection1.keras")

# Open the default camera
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    print(type(frame))
        
    input = cv2.resize(frame, (512,512))
    
    input = np.expand_dims(input, axis=0)
    result = model(input).numpy()
    result = np.asarray(result, 'float32')

    print(type(result))

    cv2.imshow('Camera', result)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == 'q':
        break

# Release the capture
cam.release()
cv2.destroyAllWindows()