import numpy as np
def vector2matrix(vector, shape):
    elementofz = int(len(vector)/shape[2])
    matrix = np.empty(shape)
    for i in range(0,shape[2]):
        matrix[:,:,i] = np.reshape(vector[i*elementofz:(i+1)*elementofz],shape[0:2], 'F')

    return matrix
