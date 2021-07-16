import numpy as np

def mart(A, b, maxIter, x0, tol):

    x = x0

    for k in range(1, maxIter):
        x1 = x

        for i in range(0, np.shape(A)[0]-1):
            theta = A[i,:]/np.linalg.norm(A[i,:])

            ratio = (b[i,0]/np.dot(A[i,:], x))**theta

            x = x*ratio

            exit()


        exit()
