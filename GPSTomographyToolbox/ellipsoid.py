import math
import numpy as np


class Ellipsoid(object):
    """!Ellipsoid class to define generic ellipsoidal coordinate system
    """

    def __init__(self):
        """!Ellipsoid initializer

        """
        pass

    @property
    def e(self):
        """!First eccentricity getter
        @return eccentrictiy (float)
        """
        return math.sqrt((self.a**2 - self.b**2)/self.a**2)
    @property
    def ec(self):
        """!Second eccentricity getter
        @return seconf eccentricity (float)
        """
        return math.sqrt((self.a**2 - self.b**2)/self.b**2)
    @property
    def f(self):
        """Flattening getter
        @return flattening (float)
        """
        return (self.a - self.b)/self.a

    def getXYZ(self, plh):
        """!Get cartesian (X,Y,Z) coordinates from geographical (longitude, latitude, altitude) coordinates
        @param plh (np.array (1,3)): geographical coordinates  [[phi, lambda, h]]
        @return XYZ_coords (np.array (1,3)): cartesian coordinates (numpy array (1,3)) [[x, y, z]]
        """
        #from point import Point
        #M = self.a*(1-self.e**2)/(1 - self.e**2*math.sin(plh.phi))**(3/2)
        N = self.a/math.sqrt(1 - self.e**2*math.sin(plh[0,0])**2)

        x = (N + plh[2,0])*math.cos(plh[0,0])*math.cos(plh[1,0])
        y = (N + plh[2,0])*math.cos(plh[0,0])*math.sin(plh[1,0])
        z = (N*(1-self.e**2) + plh[2,0])*math.sin(plh[0,0])

        return np.array([[x], [y], [z]])


    def getPLH(self, xyz):
        """!Get geographical (longitude, latitude, altitude) coordinates from cartesian (X,Y,Z) coordinates
        @param xyz (np.array (1,3)): cartesian coordinates [[x, y, z]]
        @return plt_coords (np.array (1,3)): geographical coordinates [[phi, lambda, h]]
        """
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

class WGS84(Ellipsoid):
    """!WGS84 class to define WGS84 ellipsoidal coordinate system
    """
    a = 6378137.000#meter
    b = 6356752.314#meter

class IUGG67(Ellipsoid):
    """!IUGG67 class to define IUGG67 ellipsoidal coordinate system
    """
    a = 6378160.000#meter
    b = 6356774.516#meter
