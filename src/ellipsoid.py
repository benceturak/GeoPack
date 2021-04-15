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
        if not isinstance(plh, PointPLH):
            raise TypeError("xyz must be Point type")
        #from point import Point
        #M = self.a*(1-self.e**2)/(1 - self.e**2*math.sin(plh.phi))**(3/2)
        N = self.a/(1 - self.e**2*math.sin(plh.p))**(1/2)

        x = N*math.cos(plh.p)*math.cos(plh.l)
        y = N*math.cos(plh.p)*math.sin(plh.l)
        z = N*(1-e**2)*math.sin(plh.p)

        return np.array([[x], [y], [z]])


    def getPLH(self, xyz):
        from pointxyz import PointXYZ
        if not isinstance(xyz, PointXYZ):
            raise TypeError("xyz must be PointXYZ type")
        p = math.sqrt(xyz.x**2 + xyz.y**2)
        P_l = math.atan(xyz.z/(p*(1 - self.e**2)))
        d = 1
        while abs(d) > 10**-12:

            N = self.a/math.sqrt(1 - self.e**2*math.sin(P_l)**2)
            h = p/math.cos(P_l)-N
            P = math.atan(xyz.z/(p*(1 - self.e**2*N/(N + h))))
            d = P_l - P
            P_l = P

        N = self.a/math.sqrt(1 - self.e**2*math.sin(P)**2)
        h = p/math.cos(P)-N

        L = math.atan2(xyz.y,xyz.x)



        return np.array([[P], [L], [h]])
