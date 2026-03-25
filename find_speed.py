import numpy as np

import moving_avg


def find_speed(locations, FPS):
    speed_values = []
    num_of_frames = 1
    last_location = locations[0]
    for i in range (1, len(locations)):
        if np.all(np.equal(np.array([-100000, -100000, -100000]), locations[i])):
            num_of_frames += 1
            continue
        else:
            distance = (np.sum((locations[i]-last_location) **2 ) ** 0.5)/num_of_frames
            speed_values+=[( distance * FPS) ]* num_of_frames
            num_of_frames = 1
            last_location = locations[i]
    print(f'speed values pre {speed_values}')
    speed_values = moving_avg.moving_avg(speed_values, 1)
    print(f'speed values after {speed_values}')
    return speed_values
