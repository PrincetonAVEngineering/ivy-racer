"""
Iris V1.
Assumptions: Only the road angle affects the steering direction.
Outputs: a target steering angle.
"""

from  roaddetection_angular import get_lines_from_frame
import cv2
from modules.controllers.sender import ArduinoSender
import math
import time


class Iris:
    def __init__(self, video_path):
        self.road_lines = [] #
        self.video_feed =  cv2.VideoCapture(video_path)
        self.frame = ''
        self.angle = 0
        self.cooked_counter = 0
        self.previous_angles = []
        self.angle_bias = 35 #bias term just in case camera isn't centered (in pixels)
        self.sender = ArduinoSender("COM5")
        self.sender.connect()
        self.send_counter = 0
        self.previous_angle_ints = []
        #bias term for road.mp4 is 25
        #road2.mp4 is cooked w/ this code (right railing interfering)

    #Just show the frame - not used in algorithm
    def _display_feed(self):
        """Method to display camera feed."""
        # Check if the camera opened successfully
        if not self.video_feed.isOpened():
            print("Error: Could not open video source.")
            return
        
        while True:
            # Capture frame-by-frame
            ret, frame = self.video_feed.read()

            if not ret:
                print("Failed to grab frame")
                break
             
            self.frame = frame
            # Display the resulting frame
            cv2.imshow('Camera Feed', frame)

            # Press 'q' to quit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        self.video_feed.release()
        cv2.destroyAllWindows()
        
    def get_frame(self):
        _, self.frame = self.video_feed.read()
    
    #for debug purposes
    def _play_video(self):
        """Function to play the video from self.video_feed."""
        while True:
            ret, frame = self.video_feed.read()
            if not ret:
                print("End of video or error.")
                break
            
            cv2.imshow("Video Playback", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        self.video_feed.release()
        cv2.destroyAllWindows()
    
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
        while True:
        
            self.get_frame() # sets self.frame to new frame

            # Step 2: Get road lines and intersection point
            lines, p_lines, intersection_point = get_lines_from_frame(self.frame)
            self.road_lines = lines
            self.prominent_lines = p_lines
            self.intersection_point = intersection_point

            # Step 3: Calculate steering angle from x deviation
            frame_width = self.frame.shape[1]
            center_x = frame_width // 2

            if(intersection_point[0] is None):
                self. cooked_counter += 1
                if(self.cooked_counter == 90):
                    print("we're so cooked") # lmao tomasz
                    break
                print('cooked counter', self.cooked_counter)
                continue
            
            self.cooked_counter = 0
            if intersection_point is not None:
                x, _ = intersection_point
                deviation = (x - center_x) / frame_width
                self.angle = deviation * 45  # Mapping to ±45 degrees
            else:
                self.angle = 0  # Go straight if no intersection

            # Step 4: Visualize everything
            annotated_frame = self.frame.copy()
            #Resize image for to dimensions that function resized it to to find lines
            
            scale_factor = 360 / self.frame.shape[0]
            width = int(self.frame.shape[1] * scale_factor)
            
            annotated_frame = cv2.resize(annotated_frame, (width, 360), interpolation=cv2.INTER_AREA)
            if p_lines is not None:
                for line in p_lines:
                    x1, y1, x2, y2 = line[0]
                    
                    
                    cv2.line(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if intersection_point is not None:
                x, y = map(int, intersection_point)
                cv2.circle(annotated_frame, (x, y), 6, (0, 0, 255), -1)

            # Show angle on screen
            center_x = width // 2
            

            if intersection_point is None or intersection_point[0] is None:
                continue
            else:
                x_intersect, _ = intersection_point
                x_intersect -= self.angle_bias
                deviation = (x_intersect - center_x) / width
                self.steering_angle = deviation * 45
                
                
            #5 frame moving average to reduce variance -> still not perfect -> straight line has 2 degrees off    
            self.previous_angles.append(self.angle)
            if len(self.previous_angles) > 200:
                self.previous_angles.pop(0)
            self.angle = sum(self.previous_angles) / len(self.previous_angles)
            
            cv2.putText(annotated_frame, f"Steering Angle: {self.steering_angle:.2f} deg", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv2.imshow("Iris View", annotated_frame)
            cv2.waitKey(1)
            #print("angle: inside", self.angle)
            self.send_angle_update()
            
            
            
        

    def get_steering_angle(self):
        return self.angle
    
    def send_angle_update(self):
        self.send_counter += 1
        if self.send_counter % 2 != 0:
            return

        angle_sign_bit = 1 if self.steering_angle < 0 else 0
        angle_magnitude = abs(self.steering_angle)
        angle_int = math.floor(angle_magnitude * 10)  # Scale for resolution

        # Compute current moving average before adding new value
        if self.previous_angle_ints:
            current_avg = sum(self.previous_angle_ints) / len(self.previous_angle_ints)
            if abs(angle_int - current_avg) > 8:  # Disregard outliers (> 5 deg diff)
                print(f"Ignored angle_int {angle_int} (diff > 5° from avg {current_avg})")
                return

        # Update moving average
        self.previous_angle_ints.append(angle_int)
        if len(self.previous_angle_ints) > 10:
            self.previous_angle_ints.pop(0)
        averaged_angle_int = round(sum(self.previous_angle_ints) / len(self.previous_angle_ints))
        averaged_angle_int = min(averaged_angle_int, 63)  # Clamp to 6 bits

        # Bit structure: 1 (MSB) | sign bit | 6-bit angle_int
        bit_string = (1 << 7) | (angle_sign_bit << 6) | (averaged_angle_int & 0b111111)

        # Debug prints
        print('angle:', self.angle)
        binary_str = format(bit_string, '08b')
        print('magnitude scaled:', averaged_angle_int)
        print("angle magnitude (from bits):", bit_string & 0b111111, "angle sign bit:", angle_sign_bit)
        print("binary:", binary_str)
    
    # send to arduino
        self.sender.send_data(bit_string)


    
        
def main():
    video_path = "../data/road.mp4"
    iris = Iris(video_path)
    #iris._play_video()
    iris.update()
    

if __name__ == '__main__':
    main()

    