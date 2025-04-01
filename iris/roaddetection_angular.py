
"""
TODO: 
1. Add customization for the get_lines_from_frame function. Should have variable threashold.
2. Add a better filtering system. 
   - Remove lines that are horizontal and other impossible combinations.
   - Add a y displacement to the mask
3. 
"""


import numpy as np
import cv2
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

CENTER_OFFSET = 0
RECTANGULARITY = 0.1 / 2




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

#THREASHOLD HYPERPARAMETER MAKE IT NOT COOKED
def get_most_prominent_angles(angles, num_angles=2, THREASHOLD=20):
        if angles is None or len(angles) == 0:
            return None

        angles = np.array(angles)
        angles_reshaped = angles.reshape(-1, 1)
        # Cluster the angles using DBSCAN
        db = DBSCAN(eps=10, min_samples=1).fit(angles_reshaped)
        labels = db.labels_

        # Get unique clusters and their centers
        unique_labels = np.unique(labels)
        prominent_angles = []
        indices = []

        # Sort clusters by size and get the two largest
        cluster_sizes = [(label, np.sum(labels == label)) for label in unique_labels if label != -1]
        cluster_sizes.sort(key=lambda x: x[1], reverse=True)
        largest_clusters = cluster_sizes[:num_angles]

        for label, _ in largest_clusters:
            cluster_points = angles[labels == label]
            center = np.mean(cluster_points)
            prominent_angles.append(center)
            # Get index of angle closest to center
            idx = np.argmin(np.abs(angles - center))
            indices.append(idx)
        
        return prominent_angles, indices

        prominent_angles = np.array(prominent_angles)
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


def extend_lines(lines, height):
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


def draw_road_curve(img, curve_points, color=(0, 255, 255), thickness=2):
    if curve_points is not None:
        # Draw curve as a polyline
        cv2.polylines(img, [curve_points], False, color, thickness)


def get_lines_from_frame(frame):
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

    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(contours)  # Convert tuple to list

    # Create empty mask
    filtered_roi = np.zeros_like(roi)

    # Filter contours by arc length
    for contour in contours:
        # Get contour length
        perimeter = cv2.arcLength(contour, closed=False)
        
        # Only keep long contours (adjust threshold as needed)
        if perimeter > 200:
            # Draw the contour on the mask
            cv2.drawContours(filtered_roi, [contour], -1, 255, 1)

    # Update ROI to filtered version
    roi = filtered_roi

    # Apply Sobel filter for vertical edge detection
    sobel_x = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x = np.absolute(sobel_x)
    sobel_x = np.uint8(sobel_x)

    # Update ROI with vertical edges
    roi = sobel_x

    # Hough Transform to detect lines
    lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=30, minLineLength=50, maxLineGap=100)

    """
    while not lines is None:
            print(f"threashold: {threashold}")
            lines = cv2.HoughLinesP(roi, 1, np.pi / 180, threshold=threashold, minLineLength=50, maxLineGap=100)
            print(lines)
            if lines is None or len(lines) < 2:
                threashold -= 10
                continue
            if len(lines) > 10:
                threashold += 10
                continue
            break
    """

    p_lines = get_most_prominent_lines(lines, num_lines=2)

    p_lines = extend_lines(p_lines, height)

    intersection_point = [None, None]
    # Calculate intersection point for prominent lines
    if p_lines is not None and len(p_lines) > 1:
        x1, y1, x2, y2 = p_lines[0][0]
        x3, y3, x4, y4 = p_lines[1][0]
        
        # Line equation coefficients
        a1 = y2 - y1
        b1 = x1 - x2
        c1 = a1 * x1 + b1 * y1
        
        a2 = y4 - y3
        b2 = x3 - x4
        c2 = a2 * x3 + b2 * y3
        
        # Calculate determinant
        det = a1 * b2 - a2 * b1
        
        if det != 0:
            intersection_point[0] = (b2 * c1 - b1 * c2) / det
            intersection_point[1] = (a1 * c2 - a2 * c1) / det
            # Draw intersection point
            

    return lines, p_lines, intersection_point