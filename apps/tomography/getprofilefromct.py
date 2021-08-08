def getProfileFromCT(ct, gridp, gridl, sta):

    coord = sta.getPLH[0:2,0]

    for i in range(0,np.shape(gridp)[0]-1):
        print(sta[0]*180/np.pi)
        if gridp[i] < sta[0] < gridp[i+1]:
            pi = i
    print(gridl*180/np.pi)
    for i in range(0,np.shape(gridl)[0]-1):
        print(sta[1]*180/np.pi)
        if gridl[i] < sta[1] < gridl[i+1]:
            li = i

    return ct[pi,li,:]
