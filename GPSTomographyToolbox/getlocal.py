import sys
sys.path.append("../../src/")
from ellipsoid import WGS84
import numpy as np
import point

class GetLocal(object):
    """!Transformation class from ellipsoidal coordinate system to a pre-defined cylindrical projection. 
    """
    def __init__(self, min, max):
        """!GetLocal initializer to define the corners of the area to fit the best cylinder including heights
        @param min (np.array (3,): corner of the fitted CRS
        @param max (np.array (3,): opposite corner of the fitted CRS

        """
        self.min = min
        self.max = max
        ell = WGS84()
        self.a = ell.a
        self.b = ell.b
        self.e = ell.e
        self.ec = ell.ec

    def x(self, lat):
        """!x coordinate in local coordinate system
        @param lat (float): latitude (radians)
        @return x (float): meters
        """
        M = lambda phi: self.a*(1 - self.e**2)/((1 - self.e**2*np.sin(phi)**2)**(3/2))

        x = lambda deltaPhi: M(self.min[0] + deltaPhi/2)*deltaPhi + self.a*self.e**2*(1 - self.e**2)*np.cos(2*(self.min[0] + deltaPhi/2))*deltaPhi**3*(1/8)

        return x(lat - self.min[0])
    def y(self, lon):
        """!y coordinate in local coordinate system
        @param lon (float): longitude (radians)
        @return y (float): meters
        """
        N = lambda phi: self.a*(1 - self.e**2*np.sin(phi)**2)**(-1/2)

        mid_lat = (self.min[0] + self.max[0])/2
        y = lambda deltaLam: N(mid_lat)*np.cos(mid_lat)*deltaLam

        return y(lon - self.min[1])
    def z(self, h):
        """!z coordinate in local coordinate system
        @param h (float): height (meters)
        @return z (float): meters
        """
        return h - self.min[2]

    def getLocalCoords(self, p):
        """!Transform ellipsoidal coordinates to local cylindrical coordinates
        @param p (Point, Station): Point/Station object with available geographical coordinates
        @return trnsformed_p (Point, Station): Point/Station object in  cylindrical CRS. 
        """
        plh = p.getPLH()
        x = self.x(plh[0,0])
        y = self.y(plh[1,0])
        z = self.z(plh[2,0])
        loc = np.array([x,y,z])

        if isinstance(p, point.Point):
            return point.Point(id=p.id, code=p.code, coord=loc)
        elif isinstance(p, station.Station):
            return station.Station(id=p.id, code=p.code, coord=loc)


if __name__ == "__main__":


    proj = GetLocal(np.array([45.5,15.5,0]), np.array([49.7,26.0,12000]))


    print(proj.a)
    print(proj.b)
    cc = proj.getLocalCoords(point.Point(coord=np.array([45.6,15.5,12000]), type=point.PLH, system=WGS84()))

    print(cc)
    