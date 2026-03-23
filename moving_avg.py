import numpy as np


def moving_avg(data, R):
    new_data=np.array([sum(data[:2*R+1])])
    for i in range ( R+1, len(data)-R):
        new_data = np.append(new_data, [new_data[-1]-data[i-2*R+1]+data[i+2]])
    return new_data/ (2*R+1)




