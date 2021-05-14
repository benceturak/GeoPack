import math
import numpy as np

def r(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

def diffeq(t, w, ax, ay, az):
    """
            :param w: ndarray
                    [0]: x
                    [1]: y
                    [2]: z
                    [3]: vx
                    [4]: vy
                    [5]: vz
                    [6]: ax
                    [7]: ay
                    [8]: az
    """

    aE = 6378136#m
    omegaE = 0.7292115*10**-4#rad/s
    mu = 39860044*10^14#m^3/s^2
    C20 = -1.08263*10**-3

    f1 =  w[3]
    f4 = -mu/r(w[0], w[1], w[2])**3*w[0] + 3/2*C20*mu*aE**2/r(w[0], w[1], w[2])**5*w[0]*(1-5*w[2]**2/r(w[0], w[1], w[0])**2) + ax + omegaE**2*w[0] + 2*omegaE*w[4]


    f2 = w[4]
    f5 = -mu/r(w[0], w[1], w[2])**3*w[1] + 3/2*C20*mu*aE**2/r(w[0], w[1], w[2])**5*w[1]*(1-5*w[2]**2/r(w[0], w[1], w[2])**2) + ay + omegaE**2*w[1] + 2*omegaE*w[3]




    aE = 6378136#m
    omegaE = 0.7292115*10**-4#rad/s
    mu = 39860044*10^14#m^3/s^2
    C20 = -1.08263*10**-3
    f3 = w[5]
    f6 = -mu/r(w[0], w[1], w[2])**3*w[2] + 3/2*C20*mu*aE**2/r(w[0], w[1], w[2])**5*w[2]*(1-5*w[2]**2/r(w[0], w[1], w[2])**2) + az

    return np.array([f1, f2, f3, f4, f5, f6])
