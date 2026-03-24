import numpy as np
import matplotlib.pyplot as plt

def find_closest(O, D):
    D_improved = []
    non_recognized_vector = np.array((-100000.0,-100000.0,-100000.0))
    for i in range (len(D)): #check if code found object in the frame
        if not np.array_equal(D[i], non_recognized_vector):
            D_improved.append(D[i])
    if len(D_improved)<2: #need at least 2 vecs to find aprx location
        return np.array([-100000,-100000,-100000])
    D = [D_improved[i] / np.sum(D_improved[i]*D_improved[i])**0.5 for i in range(len(D_improved))]
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


# print(find_closest(np.array([[0,0,0.1], [2,3.2,0.8], [-3,1,1.9]]), np.array([[1, 0.8, 1], [1.2,0 , 2], [1.5,0.7,0.3]]))), #
