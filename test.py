import cv2
import numpy as np
#from skimage import io, segmentation, color, measure
#from skimage import graph
#import matplotlib.pyplot as plt
last_known_direction= np.array([1,2,2])
last_known_direction = last_known_direction / (np.sum(last_known_direction * last_known_direction) ** 0.5)
print(last_known_direction)