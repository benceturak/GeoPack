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
            x[np.where(x<0.000001)] = 0.000001
        x2 = x

        err = np.abs((x2 - x1)/x2)

        #np.savetxt("err4.csv", [err], delimiter=",")
        if np.max(err) < tol:
            break
    return (x, iter)
