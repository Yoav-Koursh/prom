import cv2
import numpy as np

import calc_point
import image_cut
import moving_avg
import video_to_vector
import math
import matplotlib.pyplot as plt


R = 0.3 # distance from middle to each camera in meters
camera_angles = np.array([(1,1.9 ),(0.7549, 1.2042 ), (0.7242,1.3676), (0.7927, 1.48827),(0.488, 0.6342)])  #reinforced, HP, red, lenovo, basic
# camera_locations = [
#     # Camera 1 (top)
#     np.array((0, R, 0)),
#
#     # Camera 2
#     np.array((R * math.cos(0.1 * math.pi), R * math.sin(0.1 * math.pi), 0)),
#
#     # Camera 3
#     np.array((R * math.cos(0.5 * math.pi), R * math.sin(0.5 * math.pi), 0)),
#
#     # Camera 4
#     np.array((R * math.cos(0.9 * math.pi), R * math.sin(0.9 * math.pi), 0)),
#
#     # Camera 5
#     np.array((R * math.cos(1.3 * math.pi), R * math.sin(1.3 * math.pi), 0)),
# ]
#
#
camera_locations = [np.array([0.625,0,0]),np.array([0,0,0]),np.array([-0.68,0,0])]

# cap = cv2.VideoCapture("easytestvid.mp4")
videos = image_cut.image_cut('fulltest2.mp4', 30, 15)
direction_vectors = []
# for i in range(5):
#     direction_vectors.append(video_to_vector.find_direction_from_vid(videos[i], i))

direction_vectors.append(video_to_vector.find_direction_from_vid(videos[0], 2))
direction_vectors.append(video_to_vector.find_direction_from_vid(videos[2], 3))
direction_vectors.append(video_to_vector.find_direction_from_vid(videos[1], 0))

# for i in range (3):
#     print(i)
#     ypoints = np.append(direction_vectors[i][1], [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
#     xpoints = np.append(direction_vectors[i][0], [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2])
#     print(ypoints)
#     print(xpoints)
#     plt.plot(xpoints, ypoints)
# plt.show()
#

# plt.show()
locations = []
for i in range(len(direction_vectors[0])):
    locations.append(calc_point.find_closest(camera_locations, np.array([direction_vectors[j][i] for j in range(3)])))

