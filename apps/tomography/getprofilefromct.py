import numpy as np
from scipy import interpolate
def getProfileFromCT(ct, gridp, gridl, sta, method='nearest'):
    coord = sta.getPLH()[0:2,0]
    if method == 'nearest':


        for i in range(0,np.shape(gridp)[0]-1):
            if gridp[i] < coord[0] < gridp[i+1]:
                pi = i

        for i in range(0,np.shape(gridl)[0]-1):
            if gridl[i] < coord[1] < gridl[i+1]:
                li = i

        return ct[pi,li,:]
    elif method == 'bilinear':
        phi = np.zeros((len(gridp)-1,))
        for i in range(1,len(gridp)):
            phi[i-1] = (gridp[i] + gridp[i-1])/2

        lam = np.zeros((len(gridl)-1,))
        for i in range(1,len(gridl)):
            lam[i-1] = (gridl[i] + gridl[i-1])/2

        levels = np.shape(ct)[2]
        profile = np.zeros((levels,))

        for i in range(0, levels):
            f = interpolate.interp2d(phi, lam, ct[:,:,i].T)
            profile[i] = f(coord[0], coord[1])

        return profile
