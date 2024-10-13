import numpy as np

def matrix2vector(matrix):
    for i in range(0,len(matrix)):
        try:
            vector = np.append(vector, matrix[:,:,i].T.flatten())
        except:
            vector = matrix[:,:,i].T.flatten()

    return vector
