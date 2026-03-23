import numpy as np
from matplotlib import pyplot as plt


def find_object_locations(img): #finds border with most pixels and returns its avg location
    img_size = img.shape
    object_location = (0,0)
    most_pixels = 0
    while True:
        non_empty_pixels = np.transpose(np.nonzero(img))
        if non_empty_pixels.size == 0:
            break
        else:
            num_pixels , object_pixels = find_object_helper(img , non_empty_pixels[0],set() )

            if num_pixels > most_pixels:
                object_pixels_array = np.array([*object_pixels])
                object_location = tuple(np.sum(object_pixels_array, axis = 0)/num_pixels)
                most_pixels = num_pixels
            for index in object_pixels:
                img[index]=0
    #x = [p[1] for p in object_pixels] # + [-1920 / 2, 1920 / 2, 1920 / 2, -1920 / 2]
    #y = [-p[0] for p in object_pixels] # [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2]
    #print(num_pixels)
    # cv2.imshow("sub", sub_img)

    #plt.plot(x, y, 'o')
    #plt.show()
    object_location_vector = (object_location[0]-img_size[0]/2,object_location[1]-img_size[1]/2)
    return object_location_vector # (2*object_location_vector[0]/img_size[0], 2*object_location_vector[1]/img_size[1])


def find_object_helper(img, pixel, visited_pixels):
    counter = 1
    visited_pixels.add(tuple(pixel))

    for row_index in range(pixel[0]-5,pixel[0]+6):
        if row_index < 0 or row_index > img.shape[0] - 1:
            continue

        for column_index in range(pixel[1] - 5,pixel[1] + 6):
            if column_index < 0 or column_index > img.shape[1]-1:
                continue

            current_pixel = (row_index, column_index)
            if current_pixel not in visited_pixels and img[current_pixel[0],current_pixel[1]] == 1:
                new_count, visited_pixels = find_object_helper(img, current_pixel, visited_pixels)
                counter += new_count
    return counter, visited_pixels


#print(find_object_locations(np.array([[0,0,0,0], [0,0,0,0],[0,1,1,0],[0,1,0,0],[0,1,0,0]])))