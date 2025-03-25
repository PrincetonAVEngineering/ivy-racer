"""
Iris V1.
Assumptions: Only the road direction affects steering direction.

Functionality, identical to iris_v1, but using the blinders lane_detection model to pre-process the image
Only then should the frame be passed into the 
"""

from  modules.road_detection.roaddetection_angular import get_lines
import cv2
import numpy as np


class Iris:
    def __init__(self):
        self.road_lines = [] #
        self.angle = 0
        self.ABSOLUTE_MAX_ULTRASONIC_ANGLE = np.pi / 4 # 45 degrees.
        self.NUMBER_OF_STEPS = 10 # 10 steps per range of 2 * ABSOLUTE_MAX_ULTRASONIC_ANGLE

    def apply_blinders(self):
        pass

    def update(self):
        """
            This function represents 1 frame update. During this update, this function
            should minimally
            1. Pull a new frame from the realsense camera (or a default camera). 
            2. Pass the frame into blinders model.
            3. Apply the roaddetection function on that frame. 
            4. Use the intersection point to make a steering angle.
             - Should be something like the fraction of the frame width that the intersection point deviates 
                from the center of the screen. Should only use the x coordinate. 
            5. Store the steering angle in self.angle

            Additionally: visualize the frame with the lines and intersection point using cv2.
        """
        pass

    def get_steering_angle(self):
        return self.angle 
