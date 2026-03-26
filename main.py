from itertools import zip_longest

import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import calc_point
import image_cut
import moving_avg
import video_to_vector
import math
import matplotlib.pyplot as plt

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

    videos = image_cut.image_cut('fulltest1.mp4', 30, 15)
    locations = []
    for i in range (1,len(videos[0])):
        direction_vectors=[]
        direction_vectors.append(video_to_vector.image_to_vector(videos[0][i-1], videos[0][i],2))
        direction_vectors.append(video_to_vector.image_to_vector(videos[2][i-1], videos[2][i],3))
        direction_vectors.append(video_to_vector.image_to_vector(videos[1][i-1], videos[1][i],0))
        locations.append(calc_point.find_closest(camera_locations,direction_vectors ))


    # plt.show()
    for i in range(len(direction_vectors[0])):
    locations  = list(filter(lambda v:  not np.all(np.equal(np.array([-100000,-100000,-100000]), v)), locations))
    x_locations = [locations[i][0,0] for i in range (len(locations))]
    y_locations = [-locations[i][0,1] for i in range (len(locations))]
    z_locations = [locations[i][0,2] for i in range (len(locations))]


    print([(float(x_locations[i]), float(y_locations[i]), float(z_locations[i])) for i in range(len(locations[2:50]))])
    plt.plot(x_locations, y_locations, 'o')
    plt.show()
    plt.plot (z_locations, 'o')
    plt.show()


