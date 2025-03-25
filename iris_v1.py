"""
Iris V1.
Assumptions: Only the road angle affects the steering direction.
Outputs: a target steering angle.
"""

from  roaddetection_angular import get_lines
import cv2


class Iris:
    def __init__(self):
        self.road_lines = [] #
        self.video_feed =  cv2.VideoCapture(0) # Can change this to a video.
        self.angle = 0
        

    def update(self):
        """
            This function represents 1 frame update. During this update, this function
            should minimally
            1. Pull a new frame from the realsense camera (or a default camera). 
            2. Apply the roaddetection function on that frame. 
            3. Use the intersection point to make a steering angle.
             - Should be something like the fraction of the frame width that the intersection point deviates 
                from the center of the screen. Should only use the x coordinate. 
            4. Store the steering angle in self.angle

            Additionally: visualize the frame with the lines and intersection point using cv2.
        """
        pass

    def get_steering_angle(self):
        return self.angle 


    
