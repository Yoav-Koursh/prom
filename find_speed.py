import numpy as np

import moving_avg


def find_speed(location, last_location, FPS):
    distance = (np.sum((location-last_location) **2 ) ** 0.5)
    return  [distance * FPS]

def find_xy_speed(location, last_location, FPS):
    distance = (np.sum((location[0:2]-last_location[0:2]) **2 ) ** 0.5)
    return  distance * FPS

