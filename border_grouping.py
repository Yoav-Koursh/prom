import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
sys.setrecursionlimit(10000)

def find_object_locations(img): #finds border with most pixels and returns its avg location
    object_location = (-10000,-10000)
    most_pixels = 0
    while True:
        non_empty_pixels = np.transpose(np.nonzero(img))
        if non_empty_pixels.size == 0:
            break
        else:
            num_pixels , object_pixels = find_object_helper(img , non_empty_pixels[0],set() )
            object_pixels_array = np.array([*object_pixels]) + 0.5
            temp = np.sum(object_pixels_array, axis=0)
            temp_object_location = tuple(temp / num_pixels)

            if num_pixels > most_pixels and num_pixels > 10:# and (temp_object_location[1] > expected_loc[0] - R and temp_object_location[1]< expected_loc[0] + R) and (temp_object_location[0]> expected_loc[1] - R and temp_object_location[0] < expected_loc[1] + R):
                object_location = temp_object_location
                most_pixels = num_pixels
            for index in object_pixels:
                img[index]=0
    object_location_vector = (object_location[0],object_location[1])
    return object_location_vector, most_pixels # (2*object_location_vector[0]/img_size[0], 2*object_location_vector[1]/img_size[1])


def find_object_helper(img, pixel, visited_pixels):
    counter = 1
    r=4
    R=6
    visited_pixels.add((pixel[0], pixel[1]))

    for row_index in range(pixel[0]-R,pixel[0]+1+R):
        if row_index < 0 or row_index > img.shape[0] - 1:
            continue

        for column_index in range(pixel[1] - R,pixel[1] + 1 + R):
            if column_index < 0 or column_index > img.shape[1]-1:
                continue

            current_pixel = (row_index, column_index)
            if current_pixel not in visited_pixels and img[current_pixel[0],current_pixel[1]] == 1:
                if column_index < pixel[1] + r and  column_index > pixel[1] - r and row_index < pixel[0] + r and row_index > pixel[0] - r:
                    counter += 1
                    visited_pixels.add((row_index, column_index))
                else:
                    new_count, visited_pixels = find_object_helper(img, current_pixel, visited_pixels)
                    counter += new_count
    return counter, visited_pixels


