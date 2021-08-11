import numpy as np

def getProfileFromCT(ct, gridp, gridl, sta):

    coord = sta.getPLH()[0:2,0]

    for i in range(0,np.shape(gridp)[0]-1):
        if gridp[i] < coord[0] < gridp[i+1]:
            pi = i

    for i in range(0,np.shape(gridl)[0]-1):
        if gridl[i] < coord[1] < gridl[i+1]:
            li = i

    return ct[pi,li,:]
