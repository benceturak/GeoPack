import numpy as np

def mart(A, b, maxIter, x0, tol):

    x = x0
    for k in range(0, maxIter):
        x1 = x
        iter = k

        for i in range(0, np.shape(A)[0]-1):
            theta = A[i,:]/np.linalg.norm(A[i,:])

            ratio = np.float_power((b[i]/np.dot(A[i,:], x)),theta).T

            x = x*ratio
            err = np.abs((x - x1)/x)
        x2 = x

        err = np.abs((x2 - x1)/x2)
        print(k)
        print(np.max(err))
        if np.max(err) < tol:
            break
    ret = {}
    ret['x'] = x
    ret['iter'] = iter
    return ret
