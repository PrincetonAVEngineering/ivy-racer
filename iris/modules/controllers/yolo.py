from ultralytics import YOLO
import cv2
import pickle
import numpy as np
import os
import sys
# Disable printing


model = YOLO('yolov8n.pt')

def get_number_of_obj(result, obj_name='person'):
    detection_count = result.boxes.shape[0]

    obj_count = 0
    for i in range(detection_count):
        cls = int(result.boxes.cls[i].item())
        name = result.names[cls]
        obj_count += (int) (name == obj_name)
        continue 
        confidence = float(result.boxes.conf[i].item())
        bounding_box = result.boxes.xyxy[i].cpu().numpy()

        x = int(bounding_box[0])
        y = int(bounding_box[1])
        width = int(bounding_box[2] - x)
        height = int(bounding_box[3] - y)

    return obj_count


def get_middle(bounding_box):
    # Get the median point of a bounding box;
    # print(bounding_box)
    box_coords = bounding_box.xyxy[0] # my suspicion
    x_min, y_min, x_max, y_max = box_coords[0], box_coords[1], box_coords[2], box_coords[3]

    center_x = (x_min + x_max)/2
    center_y =  (y_min + y_max)/2

    med_point = int(center_x), int(center_y)
    return med_point

    
def get_bounding_box_area(bounding_box):
    # Calculate the area of a bounding box
    box_coords = bounding_box.xyxy[0]
    x_min, y_min, x_max, y_max = box_coords[0], box_coords[1], box_coords[2], box_coords[3]

    width = x_max - x_min
    height = y_max - y_min

    area = width * height
    return area

def sample_depth_coord(x, y, depth_frame):
    return depth_frame[x][y]

while True:
    try:
        with open("frame.pkl", "rb") as f:
            masked_color_image = pickle.load(f)

        with open("depth.pkl", "rb") as d:
            depth_image = pickle.load(d)
            
        # Add importing the depth_image here
        results = model(masked_color_image)

        width = masked_color_image.shape[0]
       
        number_of_people = get_number_of_obj(results[0])
        # print("Number of people detected: ", number_of_people, "\n")
        
        # print(annotated_frame)
        white_listed = []
        for bounding_box in results[0].boxes:
            x_mid, y_mid = get_middle(bounding_box=bounding_box)
            cls = int(bounding_box.cls.item())
            name = results[0].names[cls]
            if name != 'person':
                continue
            
            if sample_depth_coord(x_mid, y_mid, depth_frame=depth_image) <= 2.0 or True:
                white_listed.append(bounding_box)
                
        white_listed = sorted(white_listed, key = lambda x: get_bounding_box_area(x))
        
        results[0].boxes = white_listed

        # annotated_frame = results[0].plot()

        # Scale the frame to a smaller size for display
       
        person_box = white_listed[0]

        if person_box:
            x_mid, y_mid = get_middle(bounding_box=person_box)
            percent = x_mid * 100 // width
            with open('turn.pkl', 'wb') as depth_file:
                pickle.dump(percent, depth_file)

        # cv2.imshow("YOLO Real-time Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"tough: {e}")


cv2.destroyAllWindows()