import math
import numpy as np


class Ellipsoid(object):

    def __init__(self):
        pass

    @property
    def e(self):
        return math.sqrt((self.a**2 - self.b**2)/self.a**2)
    @property
    def ec(self):
        return math.sqrt((self.a**2 - self.b**2)/self.b**2)
    @property
    def f(self):
        return (self.a - self.b)/self.a

    def getXYZ(self, plh):
        #from point import Point
        #M = self.a*(1-self.e**2)/(1 - self.e**2*math.sin(plh.phi))**(3/2)
        N = self.a/(1 - self.e**2*math.sin(plh[0,0]))**(1/2)

        x = (N + plh[2,0])*math.cos(plh[0,0])*math.cos(plh[1,0])
        y = (N + plh[2,0])*math.cos(plh[0,0])*math.sin(plh[1,0])
        z = (N*(1-e**2) + plh[2,0])*math.sin(plh[0,0])

        return np.array([[x], [y], [z]])


    def getPLH(self, xyz):
        p = math.sqrt(xyz[0,0]**2 + xyz[1,0]**2)
        P_l = math.atan(xyz[2,0]/(p*(1 - self.e**2)))
        d = 1
        while abs(d) > 10**-12:

            N = self.a/math.sqrt(1 - self.e**2*math.sin(P_l)**2)
            h = p/math.cos(P_l)-N
            P = math.atan(xyz[2,0]/(p*(1 - self.e**2*N/(N + h))))
            d = P_l - P
            P_l = P

        N = self.a/math.sqrt(1 - self.e**2*math.sin(P)**2)
        h = p/math.cos(P)-N

        L = math.atan2(xyz[1,0],xyz[0,0])



        return np.array([[P], [L], [h]])
