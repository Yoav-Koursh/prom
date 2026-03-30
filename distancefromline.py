import numpy as np


def distance_from_line(o,d,p):
    if d is None or p is None:
        return 0
    op = p-o
    temp = np.cross(d,op)
    temp = np.sum(temp*temp)**0.5
    length_vector = np.sum(d*d)**0.5
    return temp/length_vector

