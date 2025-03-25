"""
Iris V1.
Assumptions: Only the ultrasonic sensor affects steering direction.
Outputs: a target steering angle.
"""

import pyserial
import cv2
import numpy as np


class Iris:
    def __init__(self):
        self.road_lines = [] #
        self.angle = 0
        self.ABSOLUTE_MAX_ULTRASONIC_ANGLE = np.pi / 4 # 45 degrees.
        self.NUMBER_OF_STEPS = 10 # 10 steps per range of 2 * ABSOLUTE_MAX_ULTRASONIC_ANGLE

    def update(self):
        """
            This function represents 1 frame update. During this update, this function
            should minimally
            1. Use the controller class to receive input from the arduino. Can add a template input 
                if the controller class is unimplemented.
            2. Calculate the angle of each step. Step zero should be -ABSOLUTE_MAX_ULTRASONIC_ANGLE and step NUMBER_OF_STEPS should be ABSOLUTE_MAX_ULTRASONIC_ANGLE
            2. Create a function that steers AWAY from close inputs. If the obstacle is dead ahead, it should prioritize moving away to the right side.
             - The obstacle can take up multiple dots / steps in the sensors output.
            
            Optionally: visualize the ultrasonic sensor data with a plot.
        """
        pass

    def get_steering_angle(self):
        return self.angle 
