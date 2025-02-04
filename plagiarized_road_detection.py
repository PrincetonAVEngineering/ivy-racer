import cv2
import numpy as np
import time

def lines_drawn(image, lines):
    blankimage = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
    
    if lines is None:
            return image
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(blankimage, (x1,y1), (x2,y2), (0,255,0), 6)
    
    image = cv2.addWeighted(image, 0.8, blankimage, 1, 0.0)
    return image

def houghlines(image):
    lines = cv2.HoughLinesP(image, 4, np.pi/180, 50, np.array([]), 40, 170)
    return lines

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    regionoi = cv2.bitwise_and(image, mask)
    return regionoi

def process_image(image):
    #Convert the image color
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #detect edges from the image
    canny = cv2.Canny(gray_image, 100, 120)

    #mask the unnecessary part
    vertices = [np.array(
        [[100,image.shape[0]],
         [250,0.68*image.shape[0]],
         [350,0.68*image.shape[0]],
         [image.shape[1]-100,image.shape[0]]],
        np.int32)]
    roi = region_of_interest(canny, vertices)

    lines = houghlines(roi)
    final = lines_drawn(image, lines)
    return final

cap = cv2.VideoCapture(0)                                                 #For real-time detection using camera
frame_counter = 0
while(True):
    flag, frame = cap.read()
    frame = cv2.resize(frame, (600,400))
    
    frame_counter += 1
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    cv2.imshow('Input', frame)
    cv2.imshow('Output', process_image(frame))
    time.sleep(0.0129)
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()