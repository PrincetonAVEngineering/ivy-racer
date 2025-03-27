import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model("blinders.keras")

# Open the default camera
cam = cv2.VideoCapture("road2.mp4")
# cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break
        
    frame_resized = cv2.resize(frame, (512,512)) / 255.0
    input = np.expand_dims(frame_resized, axis=0)
    
    result = model(input).numpy()
    result = np.squeeze(result)  # Remove batch dimension
    
    # Convert to uint8 format and ensure proper range (0-255)
    result = (result * 255).astype(np.uint8)
    
    cv2.imshow('Processed', result)
    cv2.imshow("Original", frame_resized)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cam.release()
cv2.destroyAllWindows()