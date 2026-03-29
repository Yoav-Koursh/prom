from itertools import zip_longest

import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import calc_point
import find_speed
import image_cut
import moving_avg
import video_to_vector
import math
import matplotlib.pyplot as plt
desired_fps = 15
basic_expected_error = 1000
if __name__ == '__main__':
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
    video = cv2.VideoCapture('fulltest2.mp4')
    # videos = image_cut.image_cut('fulltest1.mp4', 30, desired_fps)
    locations = []
    speeds = []
    avg_speeds = []
    last_known_location = np.array([0,0,0])
    expected_error = 200000
    frame_counter = 0
    fps_jump = 2 #basic FPS jump
    video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))-1
    prev_frames, video = image_cut.image_cut(video, fps_jump)
    frame_counter += 2*fps_jump

    while frame_counter < video_length:
        frames, video = image_cut.image_cut(video, fps_jump)
        frame_counter += fps_jump
        direction_vectors=[]
        direction_vectors.append(video_to_vector.image_to_vector(frames[0], prev_frames[0],2))#, video_to_vector.predicted_pixel(predicted_location, camera_angles[2]), expected_error))
        direction_vectors.append(video_to_vector.image_to_vector(frames[2], prev_frames[2],3))#, video_to_vector.predicted_pixel(predicted_location, camera_angles[3]), expected_error))
        direction_vectors.append(video_to_vector.image_to_vector(frames[1], prev_frames[1],0))#, video_to_vector.predicted_pixel(predicted_location, camera_angles[0]), expected_error))
        locations+=(calc_point.find_closest(camera_locations,direction_vectors ))
        prev_frames = frames
        # if locations[-1] is not None:
        #     last_known_direction = locations[-1] - last_known_location
        #     last_known_direction = last_known_direction / (np.sum(last_known_direction *last_known_direction) ** 0.5)
        #     expected_error = basic_expected_error
        #     speeds+=find_speed.find_speed(locations[-1], last_known_location, desired_fps/counter)*counter
        #     last_known_location = locations[-1]
        #     counter = 1
        # else:
        #     counter += 1
        #     expected_error = expected_error * 2
        # predicted_location = last_known_location + last_known_direction * speeds[-1] * counter / desired_fps
        # predicted_locations.append(predicted_location)
    real_locations = []
    for location in locations:
        if location is not None and location[2]<0:
            real_locations.append(location)
    print(real_locations)
    locations = np.array(real_locations)
    x_locations = [locations[i][0] for i in range (len(locations))]
    y_locations = [-locations[i][1] for i in range (len(locations))]
    z_locations = [locations[i][2] for i in range (len(locations))]
    print('real deal')
    print([(float(x_locations[i]), float(y_locations[i]), float(z_locations[i])) for i in range(len(locations))])
    # plt.plot(x_locations, y_locations, 'o')
    # plt.show()
    # plt.plot (z_locations, 'o')
    # plt.show()






