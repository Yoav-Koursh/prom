import cv2
import numpy as np
import image_cut
import moving_avg
import video_to_vector
import math
import matplotlib.pyplot as plt


R = 0.3 # distance from middle to each camera in meters
camera_angles = np.array([(1,1.9 )])
camera_locations = [
    # Camera 1 (top)
    np.array((0, R, 0)),

    # Camera 2
    np.array((R * math.cos(0.1 * math.pi), R * math.sin(0.1 * math.pi), 0)),

    # Camera 3
    np.array((R * math.cos(0.5 * math.pi), R * math.sin(0.5 * math.pi), 0)),

    # Camera 4
    np.array((R * math.cos(0.9 * math.pi), R * math.sin(0.9 * math.pi), 0)),

    # Camera 5
    np.array((R * math.cos(1.3 * math.pi), R * math.sin(1.3 * math.pi), 0)),
]




# cap = cv2.VideoCapture("easytestvid.mp4")
# videos = image_cut.image_cut('video.mp4', 30, 5)
# direction_vectors = []
# for i in range(5):
#     direction_vectors.append(video_to_vector.find_direction_from_vid(videos[i], i))



plt.show()
cv2.waitKey(0)