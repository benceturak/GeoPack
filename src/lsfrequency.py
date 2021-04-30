import numpy as np
def lsfrequency(l, minh, maxh, hstep):
    fmin = 4*np.pi*minh/l
    fmax = 4*np.pi*maxh/l
    fstep = 4*np.pi*hstep/l

    return np.arange(fmin, fmax, fstep)
