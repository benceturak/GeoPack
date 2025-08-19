import numpy as np
import point

class Line(object):
    """!Line object to to define line in 3d cartesian coordinate system

    
    """

    def __init__(self, p, alpha, e):
        """!Line initializer
        @param p (Point): point contained by the line
        @param alpha (float): angle from the axis X (azimuth) in radians
        @param e (float): elevation angle in radians
        """

        xyz = p.getXYZ()
        self.x = lambda t: xyz[0,0] + t*np.cos(alpha)*np.cos(e)
        self.y = lambda t: xyz[1,0] + t*np.sin(alpha)*np.cos(e)
        self.z = lambda t: xyz[2,0] + t*np.sin(e)

        self.xr = lambda x: (x - xyz[0,0])/(np.cos(alpha)*np.cos(e))
        self.yr = lambda y: (y - xyz[1,0])/(np.sin(alpha)*np.cos(e))
        self.zr = lambda z: (z - xyz[2,0])/np.sin(e)

    def getPointAtT(self, t):
        """!Get contained Point of the Line where 't' parameter is
        @param t (tuple)(float): list t parameters
        @return point (Point): coordinates of line
        """

        for tt in t:
            yield point.Point(coord=np.array([self.x(tt),self.y(tt),self.z(tt)]))
    def getTwhereX(self, x):
        """!Get 't' paramater of the eqations where X coordinate is
        @param x (float): X coordinate
        @return t (float): t parameter
        """
        return self.xr(x)
    def getTwhereY(self, y):
        """!Get 't' paramater of the eqations where Y coordinate is
        @param y (float): Y coordinate
        @return t (float): t parameter
        """
        return self.yr(y)
    def getTwhereZ(self, z):
        """!Get 't' paramater of the eqations where Z coordinate is
        @param z (float): Z coordinate
        @return t (float): t parameter
        """
        return self.zr(z)
