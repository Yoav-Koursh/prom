import numpy as np


def find_object_locations(img):
    object_locations = []

    while True:
        non_empty_pixels = np.transpose(np.nonzero(img))
        if non_empty_pixels.size ==0:
            break
        else:
            num_pixels , object_pixels = find_object_helper(img , non_empty_pixels[0],set() )
            object_pixels_array = np.array([*object_pixels])
            object_location = np.sum(object_pixels_array, axis = 0)/num_pixels
            object_locations.append(list(object_location))

            for index in object_pixels:
                img[index]=0
    return object_locations


def find_object_helper(img, pixel, visited_pixels):
    counter = 1
    visited_pixels.add(tuple(pixel))

    for row_index in range (pixel[0]-1,pixel[0]+2):
        if row_index < 0 or row_index > img.shape[0] - 1:
            continue

        for column_index in range(pixel[1]-1,pixel[1]+2):
            if column_index < 0 or column_index > img.shape[1]-1:
                continue

            current_pixel = (row_index, column_index)
            if current_pixel not in visited_pixels and img[current_pixel[0],current_pixel[1]] == 1:
                print(current_pixel)
                print(img[current_pixel[0],current_pixel[1]])
                new_count, visited_pixels = find_object_helper(img, current_pixel, visited_pixels)
                counter += new_count
    return counter, visited_pixels


print(find_object_locations(np.array([[1,1,1,0],[1,0,0,0],[1,0,0,1]])))