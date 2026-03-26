import numpy as np

import moving_avg


def find_speed(location, last_location, FPS):
    distance = (np.sum((location-last_location) **2 ) ** 0.5)
    return  [distance * FPS]

