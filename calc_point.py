import numpy as np
import matplotlib.pyplot as plt

def find_closest(O, D):
    D_improved = []
    for i in range (len(D)): #check if code found object in the frame
        if D[i] is not None:
            D_improved.append(D[i])
    if len(D_improved) < 2: #need at least 2 vecs to find aprx location
        return None
    D_improved = np.array (D_improved)
    D = [D_improved[i] / np.sum(D_improved[i]*D_improved[i])**0.5 for i in range(len(D_improved))]
    A = sum(np.array([np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T for i in range(len(D))]))
    b = sum(np.array([np.matmul((np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T), np.array([O[i]]).T) for i in range(len(D))]))

    A_inv = np.linalg.inv(A)

    return np.array(list(np.matmul(A_inv, b).T))


#def best_distance(O, D):
#    return sum([np.linalg.norm(np.matmul(np.identity(3) - np.matmul(D[i],D[i].T), find_closest(O, D) - O[i].T)) ** 2 for i in range(len(D))])


# def L(x, origins, directions):
#     """
#     Compute:
#         L(x) = sum_i ||(I - d_i d_i^T)(x - o_i)||^2
#
#     Parameters:
#     - x: shape (3,)
#     - origins: list/array of shape (n,3)
#     - directions: list/array of shape (n,3)
#     """
#     x = np.asarray(x, dtype=float)
#     origins = np.asarray(origins, dtype=float)
#     directions = np.asarray(directions, dtype=float)
#
#     total = 0.0
#     for o, d in zip(origins, directions):
#         total += point_to_line_squared_distance(x, o, d)
#     return total

def compute_projected_distance_sum(d, o, x):
    d = np.asarray(d)
    o = np.asarray(o)
    x = np.asarray(x)

    diff = x - o
    d_outer = d[:, :, np.newaxis] @ d[:, np.newaxis, :]
    I_3 = np.eye(3)
    projection_matrices = I_3 - d_outer
    projected = projection_matrices @ diff[:, :, np.newaxis]
    squared_norms = np.sum(projected ** 2, axis=(1, 2))
    total_sum = np.sum(squared_norms)

    return float(total_sum)
