import numpy as np
import matplotlib.pyplot as plt

def find_closest(O, D):
    D_improved = []
    for i in range (len(D)): #check if code found object in the frame
        if D[i] is not None:
            D_improved.append(D[i])
    if len(D_improved)<2: #need at least 2 vecs to find aprx location
        return None
    D_improved = np.array (D_improved)
    D = [D_improved[i] / np.sum(D_improved[i]*D_improved[i])**0.5 for i in range(len(D_improved))]
    A = sum(np.array([np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T for i in range(len(D))]))
    b = sum(np.array([np.matmul((np.identity(3) - np.array([D[i]]) * np.array([D[i]]).T), np.array([O[i]]).T) for i in range(len(D))]))

    A_inv = np.linalg.inv(A)

    return list(np.matmul(A_inv, b).T)


# print(find_closest(np.array([[0,0,0.1], [2,3.2,0.8], [-3,1,1.9]]), np.array([[1, 0.8, 1], [1.2,0 , 2], [1.5,0.7,0.3]]))), #
