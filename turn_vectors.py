import math

import numpy as np


def turn_vectors(vectors, dtheta):
    rho = np.sum(vectors[:,0:2]**2, axis=1 )**0.5
    theta = np.arctan2(vectors[:,0], vectors[:,1])
    theta+=dtheta
    vectors[:,0] = rho*np.sin(theta)
    vectors[:,1] = rho*np.cos(theta)
    return vectors

def turn_vector(v, dtheta):
    if v is None:
        return None
    rho =( v[0]*v[0]+v[1]*v[1])**0.5
    theta = np.arctan2(v[0],v[1])
    theta+=dtheta
    v[0] = rho*math.sin(theta)
    v[1] = rho*math.cos(theta)
    return v


