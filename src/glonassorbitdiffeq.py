import math
import numpy as np

ae = 6378136.0
We = 7.292115*10**-5#rad/s
mu = 3.9860044*10**14#m^3/s^2
c20 = -1.08263*10**-3

def radius(x, y, z):
    return math.sqrt(x*x+y*y+z*z);

def diffeq(t, w, axLS, ayLS, azLS):
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
    x = w[0]
    y = w[1]
    z = w[2]
    vx = w[3]
    vy = w[4]
    vz = w[5]

    r = radius(x, y, z)



    f1 = vx
    f4 = -mu/r/r/r*x+1.5*c20*mu*ae*ae/r/r/r/r/r*x*(1-5*z*z/r/r)+axLS+We*We*x+2*We*vy;

    f2 = vy
    f5 = -mu/r/r/r*y+1.5*c20*mu*ae*ae/r/r/r/r/r*y*(1-5*z*z/r/r)+ayLS+We*We*y-2*We*vx;

    f3 = vz
    f6 = -mu/r/r/r*z+1.5*c20*mu*ae*ae/r/r/r/r/r*z*(3-5*z*z/r/r)+azLS;
    return np.array([f1, f2, f3, f4, f5, f6])
