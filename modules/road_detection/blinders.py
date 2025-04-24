from tensorflow.keras.models import load_model
import cv2
import numpy as np
from skimage.color import lab2rgb, rgb2gray, rgb2lab

model = load_model("blinders.keras")

def lab_correct(img, l_factor, a_factor, b_factor):
    lab = rgb2lab(img)
    ones = np.ones_like(lab[:,:,0])
    lab[:,:,0] = lab[:,:,0] + l_factor * ones
    lab[:,:,1] = lab[:,:,1] + a_factor * ones
    lab[:,:,2] = lab[:,:,2] + b_factor * ones
    return lab2rgb(lab)

def rgb_correct(img, r_factor, g_factor, b_factor):
    ones = np.ones_like(img[:,:,0])
    img[:,:,0] = img[:,:,0] + r_factor * ones
    img[:,:,1] = img[:,:,1] + g_factor * ones
    img[:,:,2] = img[:,:,2] + b_factor * ones
    return img

def run(input):
    input = np.expand_dims(input, axis=0)
    result = model(input).numpy()
    result = np.squeeze(result) 
    return result

def make_3d(input):
    return np.stack((input, input, input), axis=-1)

# Open the default camera
cam = cv2.VideoCapture("road.mp4")
# cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break
        
    frame_resized = cv2.resize(frame, (512,512))
    filtered1 = lab_correct(frame_resized / 255.0, 0, 0, 0)
    filtered2 = lab_correct(frame_resized / 255.0, 10, -10, 15)
    filtered3 = lab_correct(frame_resized / 255.0, 10, -10, 20)
    
    result1 = run(filtered1)
    result2 = run(filtered2)
    result3 = run(filtered3)
    shown = np.concatenate((make_3d(result1), make_3d(result2), make_3d(result3), frame_resized / 255.0), axis=1)

    cv2.imshow('Outputs', shown)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cam.release()
cv2.destroyAllWindows()