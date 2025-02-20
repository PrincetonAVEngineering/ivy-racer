import numpy as np
import cv2
from sklearn.cluster import KMeans

CENTER_OFFSET = 15
RECTANGULARITY = 1 / 2

# Open video capture
video_path = r"A:\Projects\PAVE\ivy-racer\road4.mp4"  # Replace with your video file path
# For webcam, use:
# video_path = 0  # or 1, 2 depending on which camera

pipeline = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not pipeline.isOpened():
    print("Error: Could not open video.")
    exit()
    
def region_of_interest(img, vertices, type='triangle'):
    if type == 'triangle':
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image
    elif type == 'rectangle':

        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image
    
def draw_lines(img, lines, color=(0, 255, 0)):
        if lines is None:
            return
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), color, 5)
def get_line_angles(lines):
    if lines is None or len(lines) == 0:
        return None

    angles = []
    for line in lines:
        angle = np.arctan2(line[0][3] - line[0][1], line[0][2] - line[0][0]) * 180 / np.pi
        angles.append(angle)

    return angles

def get_line_positions(lines):
    if lines is None or len(lines) == 0:
        return None

    positions = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        positions.append(((x1 + x2) // 2, (y1 + y2) // 2))

    return positions

    
def get_most_prominent_lines(lines, num_lines=2):
        if lines is None or len(lines) == 0:
            return None
            
        angles = get_line_angles(lines)
        _, indices = get_most_prominent_angles(angles)
        
        prominent_lines = []
        for idx in indices:
            prominent_lines.append(lines[idx])
            
        return prominent_lines


def get_most_prominent_angles(angles, num_angles=2, THREASHOLD=10):
        if angles is None or len(angles) == 0:
            return None

        angles = np.array(angles)
        angles_reshaped = angles.reshape(-1, 1)
        
        distance_between_clusters = 0
        prominent_angles = None
        count = 42
        while (np.abs(distance_between_clusters) < THREASHOLD):

            kmeans = KMeans(n_clusters=num_angles, random_state=count)
            kmeans.fit(angles_reshaped)
            
            prominent_angles = kmeans.cluster_centers_.flatten()
            distance_between_clusters = np.diff(prominent_angles) 
            if count == 45:
                break
            if np.abs(distance_between_clusters) < THREASHOLD:
                print(angles)
            print(distance_between_clusters)
            count += 1

        # Find indices of angles closest to each cluster center
        indices = []
        for center in prominent_angles:
            idx = np.argmin(np.abs(angles - center))
            indices.append(idx)
        
        return prominent_angles, indices

def get_road_direction(lines):
    if lines is None or len(lines) == 0:
        return None


def draw_direction(img, direction):
    if direction is None or img is None:
        return
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Road Direction: {direction:.2f} degrees", (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    # Draw arrow in the center of the image
    center_x = img.shape[1] // 2
    center_y = img.shape[0] // 2
    arrow_length = 100
    angle_rad = np.radians(direction)
    end_x = int(center_x + arrow_length * np.cos(angle_rad))
    end_y = int(center_y + arrow_length * np.sin(angle_rad))
    cv2.arrowedLine(img, (center_x, center_y), (end_x, end_y), (0, 0, 255), 3)


def extend_lines(lines):
    if lines is not None:
            extended_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Calculate slope and intercept
                if x2 - x1 != 0:
                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - slope * x1
                    # Extend to bottom of frame
                    y_bottom = height
                    if slope == 0:
                        x_bottom = x1
                    else:
                        x_bottom = int((y_bottom - intercept) / slope)
                    # Extend to center height
                    y_center = height // 2
                    if slope == 0:
                        x_center = x1
                    else:
                        x_center = int((y_center - intercept) / slope)
                    extended_lines.append([[x_bottom, y_bottom, x_center, y_center]])
            return extended_lines


try:
    while True:
        # Read frames
        ret, frame = pipeline.read()
        if not ret:
            break

        # Use frame directly as color image
        # Rescale frame to 360p while maintaining aspect ratio
        scale_factor = 360 / frame.shape[0]
        width = int(frame.shape[1] * scale_factor)
        frame = cv2.resize(frame, (width, 360), interpolation=cv2.INTER_AREA)
        color_image = frame
        original_color_image = color_image.copy()
        

        # Apply sharpening using Laplacian filter
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        color_image = cv2.filter2D(color_image, -1, kernel)

        # Convert to HSV color space
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        # Get saturation channel
        saturation = hsv[:,:,1]
        # Create mask for high saturation areas
        high_sat_mask = cv2.threshold(saturation, 50, 255, cv2.THRESH_BINARY)[1]
        # Apply strong blur to high saturation areas
        blur_amount = (25,25)
        blurred = cv2.GaussianBlur(color_image, blur_amount, 0)
        color_image = np.where(high_sat_mask[:,:,None] == 255, blurred, color_image)

        # Convert to grayscale
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blur, 50, 150)

        # Define region of interest
        height, width = edges.shape
        roi_vertices = [(0, height), (0, int(height - height * RECTANGULARITY)), (width / 2 + CENTER_OFFSET, height / 2), (width, int(height - height * RECTANGULARITY)), (width, height)]
        roi = region_of_interest(edges, np.array([roi_vertices], np.int32))

        # Hough Transform to detect lines
        lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=50)

        angles = get_line_angles(lines)
        positions = get_line_positions(lines)
        prominent_angles, indexes = get_most_prominent_angles(angles)

        p_lines = get_most_prominent_lines(lines, num_lines=2)
        p_lines = extend_lines(p_lines)

        if p_lines is not None:
            avg_pos = np.mean([[(line[0][0] + line[0][2])/2, (line[0][1] + line[0][3])/2] for line in p_lines], axis=0)
        else:
            avg_pos = np.array([width//2, height//2], dtype=np.float32)
        
        # print(avg_pos)
        line_to_avg_pos = np.array([[round(avg_pos[0]), height // 2, width // 2 + CENTER_OFFSET, height]], dtype=np.int32)
        

        angle_of_avg_pos = get_line_angles([line_to_avg_pos])[0] - 180
        
        cv2.circle(original_color_image, (int(avg_pos[0]), int(avg_pos[1])), 10, (255, 0, 0), -1)

        road_direction = np.sum(prominent_angles) + 90
        draw_direction(original_color_image, angle_of_avg_pos)

        # Draw lines on the original image
        draw_lines(original_color_image, p_lines, color=(0, 255, 0))
        draw_lines(original_color_image, lines, color=(255, 0, 0))
        draw_lines(original_color_image, [line_to_avg_pos], color=(0, 0, 255))

        # Show images
        cv2.imshow('Road Detection', original_color_image)
        cv2.imshow("region of interest", roi)
        # Create video writer if it doesn't exist
        if 'out' not in locals():
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width, height))
        
        # Write frame to video
        out.write(original_color_image)
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the capture
    pipeline.release()
    cv2.destroyAllWindows()