import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares


def locate(rays):
    """
    Determine the closest point to an arbitrary number of rays, and optionally plot the results

    :param rays:    list of ray tuples (S, D) where S is the starting point & D is a unit vector
    :return:        scipy.optimize.OptimizeResult object from scipy.optimize.least_squares call
    """

    # Generate a starting position, the dimension-wise mean of each ray's starting position
    ray_start_positions = []
    for ray in rays:
        ray_start_positions.append(ray[0])
    starting_P = np.stack(ray_start_positions).mean(axis=0).ravel()

    # Start the least squares algorithm, passing the list of rays to our error function
    ans = least_squares(distance, starting_P, kwargs={'rays': rays})

    return ans


def distance(P, rays):
    """
    Calculate the distance between a point and each ray

    :param P:       1xd array representing coordinates of a point
    :param rays:    list of ray tuples (S, D) where S is the starting point & D is a unit vector
    :return:        nx1 array of closest distance from point P to each ray in rays
    """

    dims = len(rays[0][0])

    # Generate array to hold calculated error distances
    errors = np.full([len(rays)*dims,1], np.inf)

    # For each ray, calculate the error and put in the errors array
    for i, _ in enumerate(rays):
        S, D = rays[i]
        t_P = D.dot((P - S).T)/(D.dot(D.T))
        if t_P > 0:
            print(i*dims, (i+1)*dims)
            errors[i*dims:(i+1)*dims] = (P - (S + t_P * D)).T
        else:
            errors[i*dims:(i+1)*dims] = (P - S).T

    # Convert the error array to a vector (vs a nx1 matrix)
    return errors.ravel()


def find_closest(O, D):
    D = [D[i] / np.sum(D[i]*D[i])**0.5 for i in range(len(D))]
    A = sum(np.array([np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T for i in range(len(D))]))
    b = sum(np.array([np.matmul((np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T), np.array([O[i]]).T) for i in range(len(D))]))
    #print(np.array([D[0]]) * np.array([D[0]]).T)
    #print('A:\n',A,'\n\n')
    #print('b:\n',b,'\n\n')
    #print((np.identity(3) - np.array([D[0]]) * np.array([D[0]]).T), '\n\n', np.array([O[0]]).T, '\n\n', np.array([O[0]]), '\n\n', (np.identity(3) - np.array([D[0]]) * np.array([D[0]]).T) * np.array([O[0]]).T, '\n\n', (np.identity(3) - np.array([D[0]]) * np.array([D[0]]).T) * np.array([O[0]]))
    #print('\n\n', A, '\n\n')
    #print(B,'\n\n')
    # return np.linalg.solve(A, B)
    A_inv = np.linalg.inv(A)

    return np.matmul(A_inv, b).T


print(find_closest(np.array([[0,0,0.1], [2,3.2,0.8], [-3,1,1.9]]), np.array([[1, 0.8, 1], [1.2,0 , 2], [1.5,0.7,0.3]]))), #
