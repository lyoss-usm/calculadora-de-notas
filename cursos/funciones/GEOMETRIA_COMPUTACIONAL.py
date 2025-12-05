import numpy as np

def NP(x):
    w = np.array([0.4, 0.2, 0.1, 0.1, 0.1, 0.1])

    return np.dot(x, w)
