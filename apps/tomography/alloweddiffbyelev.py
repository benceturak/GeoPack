import numpy as np

def allowedDiffByElev(ez):
    elev = [10,90]
    diff = [0.06, 0.006]
    #ez = np.array([[10],[20],[30],[40],[50],[60],[70],[80],[90]])
    return np.interp(ez,elev,diff)

