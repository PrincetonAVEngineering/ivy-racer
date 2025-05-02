import pyrealsense2 as rs
import numpy as np
import cv2
from sender import ArduinoSender
import time

def main():
    # Configure depth stream
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

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

            print(f"Center distance: {center_distance:.3f} meters")

            throttle = int(max( min( center_distance * 10 , 20), 0))
            throttle_byte = int(throttle).to_bytes(1, byteorder='big', signed=False)

            sender.send_data(throttle_byte)

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        # Stop streaming
        pipeline.stop()

if __name__ == "__main__":
    main()