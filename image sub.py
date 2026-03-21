import cv2
import copy

# Load the video file
cap = cv2.VideoCapture("ball_rolling.mp4")
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Check if the video opened correctly
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read and display video frames
random_frame = 0
n = 0
while True:
    n += 1
    ret, frame1 = cap.read()

    if not ret:
        break   # No more frames -> exit loop

    ret, frame2 = cap.read()

    if not ret:
        break

    sub = cv2.subtract(frame1, frame2)
    cv2.imshow("Video", sub)

    if n == frame_count // 2:
        random_frame = copy.deepcopy(sub)

    # Press Q to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.imshow("rand", random_frame)
cv2.waitKey(0)

# Release resources
cap.release()
cv2.destroyAllWindows()