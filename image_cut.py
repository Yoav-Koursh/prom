# Source - https://stackoverflow.com/a/70125364
# Posted by manaclan, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-21, License - CC BY-SA 4.0

import cv2
import numpy as np

"""img = cv2.imread('imtest1.JPG')
H,W = img.shape[:2]
cv2.waitKey(0)
cropped = img[0:H//2, 0:W//2]
#cv2.imshow('image',image)
cv2.imshow('image',img)
cv2.imshow('cropped',cropped)
cv2.waitKey(0)

#cv2.imwrite('res.jpg',new_img)
#print(image.shape, new_img.shape)
input()"""

import cv2

# Load the video file
cap = cv2.VideoCapture("video.mp4")

# Check if the video opened correctly
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

cut_videos = [[],[],[],[],[]]
n = 0
# Read and display video frames
while True:
    n += 1
    if n % 20 == 0:
        print(n)
    ret, frame = cap.read()

    if not ret:
        break   # No more frames -> exit loop

    # cv2.imshow("Video", frame)

    H, W = frame.shape[:2]
    cuts = []
    cut_h, cut_w = H // 5, W // 5
    for i in range(5):
        cut_videos[i].append(frame[:, cut_w*i:cut_w*(i+1)])

    # Press Q to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()