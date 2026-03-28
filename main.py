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


desired_fps =2

REINFORCED_INDEX, HP_INDEX, RED_INDEX, LENOVO_INDEX, BASIC_INDEX = 0, 1, 2, 3, 4

if __name__ == '__main__':
    # R = 0.3 # distance from middle to each camera in meters
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
    camera_locations = [np.array([-4.1,-4.05,0]), np.array([4.05,-4.2,0]),np.array([5.6,0,0])]

    # videos = image_cut.extract_frames(["test1\\hp(-300,-262).mp4", "test1\\lenovo(374,0).mp4", "test1\\reinfourced(80,463).mp4"], 30, 5, 58 * 30, 62 * 30) # image_cut.image_cut('fulltest2.mp4', 30, desired_fps)
    videos = image_cut.image_cut('videos/drone1-1.5.mp4', 30,desired_fps)
    print(len(videos[0]))
    direction_vectors = []

    # for i in range(5):
    #     direction_vectors.append(video_to_vector.find_direction_from_vid(videos[i], i))

    direction_vectors.append(video_to_vector.find_direction_from_vid(videos[0], HP_INDEX))
    direction_vectors.append(video_to_vector.find_direction_from_vid(videos[1], LENOVO_INDEX))
    direction_vectors.append(video_to_vector.find_direction_from_vid(videos[2], REINFORCED_INDEX))
    direction_vectors[2] = -direction_vectors[2]
    # plt.show()
    locations = []
    for i in range(min([len(k) for k in direction_vectors])):
        locations.append(calc_point.find_closest(camera_locations, np.array([direction_vectors[j][i] for j in range(len(direction_vectors))])))

    locations  = list(filter(lambda v:  not np.all(np.equal(np.array([-100000,-100000,-100000]), v)), locations))
    x_locations = [locations[i][0,0] for i in range (len(locations))]
    y_locations = [-locations[i][0,1] for i in range (len(locations))]
    z_locations = [locations[i][0,2] for i in range (len(locations))]
    with open('results.txt', 'w') as file:
        for i in range(len(locations)):
            file.write(str((float(x_locations[i]), float(y_locations[i]), float(z_locations[i])))+',')
    plt.plot(x_locations, y_locations, 'o')
    plt.show()
    plt.plot (z_locations, 'o')
    plt.show()
    speed_values = find_speed.find_speed(locations, desired_fps)
    plt.plot(speed_values, 'o')
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()