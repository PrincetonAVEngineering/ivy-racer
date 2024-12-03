import torch
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

camera_index = 0
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print("Error: Camera not accessible. Please check your camera connection and permissions.")
    exit()


while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Real-time Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()