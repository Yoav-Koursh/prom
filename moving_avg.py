import numpy as np

def moving_avg(data, R):
    window_size = 2 * R + 1
    weights = np.ones(window_size)/window_size
    sma = np.convolve(data, weights, mode = 'valid')
    return sma

data = np.array([1,2,3,2,1,1,1,3,3,3])
