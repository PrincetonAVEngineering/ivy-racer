"""
Iris V1.
Assumptions: Only the road angle affects the steering direction.
Outputs: a target steering angle.
"""

from  roaddetection_angular import get_lines_from_frame
import cv2


class Iris:
    def __init__(self):
        self.road_lines = [] #
        self.video_feed =  cv2.VideoCapture("/data/road.mp4")
        self.frame = ''
        self.angle = 0

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
        ret, self.frame = self.video_feed.read()
        if not ret:
            print("you're cooked")
            return
    

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
        self.get_frame(self) # sets self.frame to new frame

        # Step 2: Get road lines and intersection point
        lines, p_lines, intersection_point = get_lines_from_frame(self.frame)
        self.road_lines = lines
        self.prominent_lines = p_lines
        self.intersection_point = intersection_point

        # Step 3: Calculate steering angle from x deviation
        frame_width = self.frame.shape[1]
        center_x = frame_width // 2

        if intersection_point is not None:
            x, _ = intersection_point
            deviation = (x - center_x) / frame_width
            self.angle = deviation * 45  # Mapping to ±45 degrees
        else:
            self.angle = 0  # Go straight if no intersection

        # Step 4: Visualize everything
        annotated_frame = self.frame.copy()

        if p_lines is not None:
            for line in p_lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if intersection_point is not None:
            x, y = map(int, intersection_point)
            cv2.circle(annotated_frame, (x, y), 6, (0, 0, 255), -1)

        # Show angle on screen
        cv2.putText(annotated_frame, f"Steering Angle: {self.angle:.2f} deg", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Iris View", annotated_frame)
        cv2.waitKey(1)
        
        pass

    def get_steering_angle(self):
        return self.angle


def main():
    iris = Iris()
    iris._display_feed()
    

if __name__ == '__main__':
    main()

    
