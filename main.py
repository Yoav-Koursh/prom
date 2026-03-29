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
    camera_locations = [np.array([-3.4,0,0]),np.array([0,5.6,0]),np.array([2.1,0,0])]
    video = cv2.VideoCapture('dronefootage2.mp4')
    # videos = image_cut.image_cut('fulltest1.mp4', 30, desired_fps)
    locations = []
    # video.set(cv2.CAP_PROP_POS_FRAMES, 20)
    fps_jump = 10 #basic FPS jump
    frames_counter = 0
    # video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))-1
    for i in range (30*28):
        print(i)
        a,b = video.read()
    #print(video_length)
    prev_frames, video = image_cut.image_cut(video, fps_jump)
    frames_counter += fps_jump
    while frames_counter<80 :
        frames, video = image_cut.image_cut(video, fps_jump)
        if frames is None:
            break
        direction_vectors=[]
        new_direction_vec, n_pixels1 = video_to_vector.image_to_vector(frames[0], prev_frames[0],1)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[2]), expected_error))
        new_direction_vec, n_pixels2 = video_to_vector.image_to_vector(frames[1], prev_frames[1],3)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[3]), expected_error))
        new_direction_vec, n_pixels3 = video_to_vector.image_to_vector(frames[2], prev_frames[2],0)
        direction_vectors.append(new_direction_vec)#, video_to_vector.predicted_pixel(predicted_location, camera_angles[0]), expected_error))
        new_loc =calc_point.find_closest(camera_locations,direction_vectors )
        if new_loc is not None and new_loc[0][2]<0:
            locations+=new_loc
            if len(locations)>1:
                xy_speed = find_speed.find_xy_speed(locations[-1], locations[-2], 30/fps_jump)
                object_pixel_num = max(n_pixels1, n_pixels2, n_pixels3)
                object_pixel_radius = object_pixel_num/(2*3.14)
                object_radius = (object_pixel_radius/ 1920)* new_loc[0][2] * math.tan(1.9)
                fps_jump = int(object_radius * 30 // xy_speed) + 1
                print(fps_jump)
                # print(f'num frames left{video_length - frame_counter}')
        frames_counter += fps_jump
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

    print(locations)
    locations = np.array(locations)
    x_locations = [locations[i][0] for i in range (len(locations))]
    y_locations = [-locations[i][1] for i in range (len(locations))]
    z_locations = [locations[i][2] for i in range (len(locations))]
    print('real deal')
    print([(float(x_locations[i]), float(y_locations[i]), float(z_locations[i])) for i in range(len(locations))])
    # plt.plot(x_locations, y_locations, 'o')
    # plt.show()
    # plt.plot (z_locations, 'o')
    # plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()






