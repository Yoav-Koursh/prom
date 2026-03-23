import numpy as np

def moving_avg(data, R):
    window_size = 2*R+1
    weights = np.ones(window_size)/window_size
    sma = np.convolve(data, weights, mode = 'valid')
    return sma
