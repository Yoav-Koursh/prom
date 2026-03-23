import numpy as np
from numpy.linalg import linalg


def vector_meeting(direction_vectors, origin_vectors):
    A= np.zeros((3,3))
    for i in range(len(direction_vectors)):
        print(A)
        # print( f' direction: {np.array([direction_vectors[i]])}, transposed_direction { np.transpose(np.array([direction_vectors[i]]))}')
        A = A + np.cross(np.array([direction_vectors[i]]) , np.transpose(np.array([direction_vectors[i]])), axis=0)
    print(A)
    B = np.sum ([(np.identity(3) - np.dot(direction_vectors[i], np.transpose(np.array([direction_vectors[i]]))))* origin_vectors[i] for i in range(len(direction_vectors))], axis=0)
    inverse_A = np.linalg.inv(A)
    return np.dot(inverse_A ,B)

direction = np.array([[1,0,0],[0,1,0]])
origin = np.array([[0,1,0], [1,0,0]])
vector_meeting(direction, origin)