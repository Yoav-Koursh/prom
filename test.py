# import copy
# from itertools import zip_longest
#
# import cv2
# import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
#
# import calc_point
# import find_speed
# import image_cut
# import moving_avg
# import video_to_vector
# import math
# import matplotlib.pyplot as plt
# desired_fps = 15
# basic_expected_error = 1000
# if __name__ == '__main__':
#     R = 0.3 # distance from middle to each camera in meters
#     # camera_angles = np.array([(1,1.9 ),(0.7549, 1.2042 ), (0.7242,1.3676), (0.7927, 1.48827),(0.488, 0.6342)])  #reinforced, HP, red, lenovo, basic
#     # camera_locations = [
#     #     # Camera 1 (top)
#     #     np.array((0, R, 0)),
#     #
#     #     # Camera 2
#     #     np.array((R * math.cos(0.1 * math.pi), R * math.sin(0.1 * math.pi), 0)),
#     #
#     #     # Camera 3
#     #     np.array((R * math.cos(0.5 * math.pi), R * math.sin(0.5 * math.pi), 0)),
#     #
#     #     # Camera 4
#     #     np.array((R * math.cos(0.9 * math.pi), R * math.sin(0.9 * math.pi), 0)),
#     #
#     #     # Camera 5
#     #     np.array((R * math.cos(1.3 * math.pi), R * math.sin(1.3 * math.pi), 0)),
#     # ]
#     #
#     #
#     camera_locations = [np.array([0,-1,0]),np.array([0,0 ,0]),np.array([0,1,0])]
#     video = cv2.VideoCapture('dronefootage2.mp4')
#     # videos = image_cut.image_cut('fulltest1.mp4', 30, desired_fps)
#     locations = np.array([[0,1920/2], [0,0],[0,-1920/2]])
#     direction_vectors=[]
#     for i in range(2):
#         centered_location = locations[i]
#         direction_vector = centered_location / np.array([540, 1920 / 2]) * np.tan(math.pi / 4)
#         direction_vector_3d = [direction_vector[0], direction_vector[1], 1]
#         direction_vector_3d = np.array(direction_vector_3d)
#         direction_vector_3d = direction_vector_3d / (np.sum(direction_vector_3d * direction_vector_3d)) ** 0.5
#         direction_vectors.append(direction_vector_3d)
#
#
#     new_loc =calc_point.find_closest(camera_locations,direction_vectors )

import numpy as np


def real_img_to_vec(frame_loc, u, v, camera_angles):
    real_x = (frame_loc[0] - 1920 / 2) / (1920 / 2) * np.tan(camera_angles[1] / 2)
    real_y = (frame_loc[1] - 1080 / 2) / (1080 / 2) * np.tan(camera_angles[0] / 2)
    x_vec_2 = u * real_x
    y_vec_2 = v * real_y
    D = x_vec_2 + y_vec_2 + np.cross(u, v)

    return D