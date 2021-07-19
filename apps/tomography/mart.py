import numpy as np

def mart(A, b, maxIter, x0, tol):

    x = x0
    for k in range(1, maxIter):
        print(k)
        x1 = x
        iter = k

        for i in range(0, np.shape(A)[0]-1):
            theta = A[i,:]/np.linalg.norm(A[i,:])



            ratio = np.float_power((b[i]/np.dot(A[i,:], x)),theta).T
            if b[i] == 0:
                exit()


            x = x*ratio
        x2 = x
        

        err = np.abs((x2 - x1)/x2)
        print(np.max(err))
        print('------------------------')
        if np.max(err) < tol:
            break
    ret = {}
    ret['x'] = x
    ret['iter'] = iter
    return ret
