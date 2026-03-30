import math

import cv2
import numpy as np
from matplotlib.pyplot import imshow

import border_grouping
import image_distort
import matplotlib.pyplot as plt

import moving_avg

# camera_angles = np.array([(1,1.9 ),(0.7549, 1.2042 ), (0.7242,1.3676), (0.7927, 1.48827),(0.488, 0.6342)])  #reinforced, HP, red, lenovo, basic
camera_angles = np.array([(1.1781, 2.0944), (0.7875, 1.4), (0.7242, 1.3676), (0.93265875, 1.65806), (0.488, 0.6342)])


def find_edges(img):
    thresh = 30
    img_blur = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    edges_arr = np.array(edges)
    edges_arr = edges_arr // 255
    return edges_arr


def image_to_vector(img1, img2, camera_index):
    img2 = image_distort.correct_image(img2, camera_index)
    img1 = image_distort.correct_image(img1, camera_index)
    current_subtracted_frame = cv2.subtract(img1, img2)
    b, g, r = cv2.split(current_subtracted_frame)
    # cv2.imshow('imga', img1)
    # cv2.imshow('imgb', img2)
    # cv2.imshow('subtract', current_subtracted_frame)
    edges_arr = find_edges(current_subtracted_frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    object_location, n_pixels = border_grouping.find_object_locations(edges_arr)
    if object_location == (-10000,-10000):
        return None , 0, (0,0)
    centered_location = (object_location - np.array([540, 1920 / 2])) * np.array([-1, 1])
    direction_vector = centered_location  / np.array([540, 1920 / 2]) * np.tan(camera_angles[camera_index] / 2)
    direction_vector_3d = [direction_vector[0], direction_vector[1], 1]
    direction_vector_3d = np.array(direction_vector_3d)
    direction_vector_3d = direction_vector_3d / (np.sum(direction_vector_3d*direction_vector_3d))**0.5
    # print(direction_vector_3d)
    return direction_vector_3d, n_pixels, object_location

#
# def find_direction_from_vid(video, camera_index):
#
#     object_locations = image_to_vector(video, camera_index)
#     object_locations_map = np.array([ 1 if a != (0,0) else 0 for a in list(object_locations)])
#     # plt.plot(direction_vector[1], direction_vector[0], 'o')
#     ypoints = [-loc[0] + 540 for loc in object_locations] + [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2] # np.append(smooth_object_location[1], [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
#     xpoints = [loc[1] - 1920 / 2 for loc in object_locations] + [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2]# np.append(smooth_object_location[0], [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2])
#     plt.plot(xpoints, ypoints, 'o')
#     plt.show()
#     direction_vector_3d = np.array([direction_vector_3d[i] if object_locations_map[i] else np.array((-100000,-100000,-100000))for i in range (len(object_locations_map))])
#     return direction_vector_3d

    # viewing the data

    xpoints = np.array([i[1] - (1920 / 2) for i in object_locations] + [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
    ypoints = np.array([-i[0] + (540) for i in object_locations] + [-1080 / 2, 1080 / 2, 1080 / 2, -1080 / 2])
    plt.plot(xpoints, ypoints, 'o')

    xavgpoints = np.array([i[1] for i in smooth_object_location] + [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
    yavgpoints = np.array([i[0] for i in smooth_object_location] + [-1080 / 2, 1080 / 2, 1080 / 2, -1080 / 2])
    plt.plot(xpoints, ypoints)
    plt.plot(xavgpoints, yavgpoints, 'o')

# vid =cv2.VideoCapture('testvid3.mp4')
# find_direction_from_vid(vid, 0)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def predicted_pixel(v, a):
    print(f'og prediction {v}')
    v = np.array(v)
    v = v/v[2]
    if v[0] == 0:
        prediction_x = 0
    else:
        prediction_x = 1920*math.tan(a[0]/2)/(2*v[0])
    if v[1] == 0:
        prediction_y = 0
    else:
        prediction_y= 1080*math.tan(a[1]/2)/(2*v[1])
        print (f' pridiction x{ prediction_x}, prediction y {prediction_y}')
    return (prediction_y, prediction_x)

