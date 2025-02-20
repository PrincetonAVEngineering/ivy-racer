## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import pickle

max_distance = 999999999


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
                # Wait for frames
        frames = pipeline.wait_for_frames()

        # Align depth frame to color frame
        align = rs.align(rs.stream.color)
        aligned_frames = align.process(frames)

        # Get depth and color frames
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        
        # Convert frames to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Create a mask based on the depth threshold
        depth_scale = pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        max_distance_in_mm = max_distance / depth_scale  # Convert max distance to depth units
        mask = (depth_image <= max_distance_in_mm).astype(np.uint8)  # 1 where depth <= max_distance

        mask_function = lambda x, y: x * y  
        
        #print(color_image.shape)
        #print(depth_image.shape)
        depth_image = np.power(depth_image, 0.16)

        # shady_image = np.multiply(color_image , 1 / np.stack([depth_image, depth_image, depth_image], axis=-1))

        #shady_image = map(mask_function, color_image, )
        #print(list(shady_image))

        #map()

        # Apply the mask to the color image
        masked_color_image = cv2.bitwise_and(color_image, color_image, mask=mask)


        # Visualize
    
        # cv2.imshow("Color Image", color_image)
        # cv2.imshow("Masked Color Image", masked_color_image)

        with open("frame.pkl", "wb") as f:
            pickle.dump(color_image, f)


        with open("depth.pkl", "wb") as d:
            pickle.dump(depth_image, d)
        
        

        # Add exporting the depth_image to depth.pkl

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        continue

        

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # TO DO: mask the color_image based on the depth_image. 

        mask = np.where(depth_image > 1000, 0, 1)
        # mask = depth_image / 65536.0

        triple_mask = np.stack([mask, mask, mask], axis=-1).astype('float32')
        # print(np.max(triple_mask))

        #print(color_image)
        masked_image = np.multiply(triple_mask, color_image)
        masked_image = masked_image + 0.1 * color_image/255.0

        normalized_image = cv2.normalize(masked_image, None, 0, 1, cv2.NORM_MINMAX)
        image_to_display = normalized_image.astype('uint8')
                
        #https://prod.liveshare.vsengsaas.visualstudio.com/join?9945B04F9FBE858262E67F34F7AF71BE217C

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', masked_image)
        cv2.waitKey(1)

        continue

        #print(masked_image)


        
        #masked_color_image = np.where(mask == True, color_image, )


        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()