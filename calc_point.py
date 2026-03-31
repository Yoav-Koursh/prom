import numpy as np


def find_closest(O, D):
    # 1. Filter out None values from BOTH O and D so indices match
    valid_indices = [i for i, d in enumerate(D) if d is not None]

    if len(valid_indices) < 2:
        return None

    # Filtered arrays
    O_filt = np.array([O[i] for i in valid_indices])
    D_filt = np.array([D[i] for i in valid_indices])

    # 2. Normalize directions (with safety epsilon to avoid divide by zero)
    # This prevents the sqrt/NaN issues
    norms = np.linalg.norm(D_filt, axis=1, keepdims=True)
    D_norm = D_filt / (norms + 1e-9)

    # 3. Build A and b using the least squares intersection of lines formula
    # Formula: A = sum(I - d*d.T), b = sum((I - d*d.T) * o)
    I = np.identity(3)
    A = np.zeros((3, 3))
    b = np.zeros(3)

    for i in range(len(D_norm)):
        # .flatten() ensures the shape is (3,) exactly
        d = D_norm[i].flatten()
        o = O_filt[i].flatten()

        # Projection matrix: (I - d*d.T)
        # np.outer(d, d) correctly creates the 3x3 matrix
        proj = I - np.outer(d, d)

        A += proj
        b += proj @ o  # '@' is the shorthand for np.matmul

    # 4. Solve Ax = b
    try:
        x = np.linalg.solve(A, b)
        return x
    except np.linalg.LinAlgError:
        # In case A is singular (lines are all parallel)
        return None


def compute_projected_distance_sum(d, o, x):
    """
    Computes the sum of squared distances from point x to the lines
    defined by origins o and directions d.
    """
    if x is None: return np.inf

    d = np.asarray(d)
    o = np.asarray(o)
    x = np.asarray(x)

    # Ensure d is normalized
    d_norms = np.linalg.norm(d, axis=1, keepdims=True)
    d = d / (d_norms + 1e-9)

    # Vector from origin to point x
    diff = x - o

    # Distance from point to line: ||(x - o) - ((x - o)·d)d||^2
    # Which is the same as: || (I - d*d.T) * (x - o) ||^2
    total_sum = 0
    for i in range(len(d)):
        proj_matrix = np.identity(3) - np.outer(d[i], d[i])
        dist_vec = proj_matrix @ diff[i]
        total_sum += np.sum(dist_vec ** 2)

    return float(total_sum)