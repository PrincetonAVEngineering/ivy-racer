import pyrealsense2 as rs
import numpy as np
import cv2
from sender import ArduinoSender
import time
import pickle
import os

def main():
    # Configure depth stream
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # <-- Add this line


    # Start streaming
    pipeline.start(config)

    sender = ArduinoSender("COM5")
    sender.connect()

    try:
        while True:
            # Wait for a coherent pair of frames: depth
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            # Save depth frame to a pickle file
            with open('depth.pkl', 'wb') as depth_file:
                depth_data = np.asanyarray(depth_frame.get_data())
                pickle.dump(depth_data, depth_file)

            
            


            # Save color frame to a pickle file (if available)
            color_frame = frames.get_color_frame()
            if color_frame:
                with open('frame.pkl', 'wb') as color_file:
                    color_data = np.asanyarray(color_frame.get_data())
                    pickle.dump(color_data, color_file)
            # Convert depth frame to numpy array
            depth_image = np.asanyarray(depth_frame.get_data())
            # Display the depth frame using OpenCV
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            cv2.imshow('Depth Frame', depth_colormap)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Get distance at the center of the image
            # Remove the bottom 33% of the frame
            height, width = depth_image.shape
            crop_height = int(height * 2 / 3)
            depth_image = depth_image[:crop_height, :]
            height, width = depth_image.shape
            # Calculate the average distance of the entire image
            # Crop the depth image to a center vertical rectangle
            crop_width = width // 2
            start_x = (width - crop_width) // 2
            cropped_depth_image = depth_image[:, start_x:start_x + crop_width]
            # Crop the depth image to a center vertical rectangle
            crop_height = height // 3
            start_y = (height - crop_height) // 2
            cropped_depth_image = cropped_depth_image[start_y:start_y + crop_height, :]
            valid_distances = cropped_depth_image[cropped_depth_image > 0]  # Exclude zero values

            if valid_distances.size > 0:
                center_distance = np.min(valid_distances) / 1000
                center_distance = np.percentile(valid_distances, 25) / 1000
            else:
                center_distance = 0
            
            # center_distance = depth_frame.get_distance(width // 2, height // 2)

            # print(f"Center distance: {center_distance:.3f} meters")

            throttle = int(max( min( (center_distance - 1.5) * 64 , 127), 0))
            throttle_byte = int(throttle)
            # print(f"throttle: {throttle_byte}")

            import os
            if os.path.exists("turn.pkl"):
                with open("turn.pkl", "rb") as d:
                    try:
                        turn = pickle.load(d)
                    except Exception as e:
                        print("oops", e)
            else:
                print("turn.pkl not found")
                continue  # or set a default value and continue
            
            turn = (int(turn) - 50)

            # print(f"turn: {turn}")

            angle_sign_bit = int(turn < 0)
            bit_string = (1 << 7) | (angle_sign_bit << 6) | (abs(turn) & 0b111111)

            sender.send_data(throttle_byte)
            time.sleep(0.05)
            sender.send_data(bit_string)
            time.sleep(0.05)
            

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        # Stop streaming
        pipeline.stop()
        sender.disconnect()

if __name__ == "__main__":
    main()