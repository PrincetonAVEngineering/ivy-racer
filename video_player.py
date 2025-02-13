import cv2
from trainsegment import get_masked_frame


# Open video file
video_path = "Videos/road_video1.mp4"
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read and display frames
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("End of video or error reading frame.")
        break

    cv2.imshow("Video", get_masked_frame(frame))

    # Press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()