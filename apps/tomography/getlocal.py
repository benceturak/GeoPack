from ellipsoid import WGS84
import numpy as np
import point

class GetLocal(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max
        ell = WGS84()
        self.a = ell.a
        self.b = ell.b
        self.e = ell.e
        self.ec = ell.ec

    def x(self, lat):
        M = lambda phi: self.a*(1 - self.e**2)/((1 - self.e**2*np.sin(phi)**2)**(3/2))

        x = lambda deltaPhi: M(self.min[0] + deltaPhi/2)*deltaPhi + self.a*self.e**2*(1 - self.e**2)*np.cos(2*(self.min[0] + deltaPhi/2))*deltaPhi**3*(1/8)

        return x(lat - self.min[0])
    def y(self, lon):
        N = lambda phi: self.a*(1 - self.e**2*np.sin(phi)**2)**(-1/2)

        mid_lat = (self.min[0] + self.max[0])/2
        y = lambda deltaLam: N(mid_lat)*np.cos(mid_lat)*deltaLam

        return y(lon - self.min[1])
    def z(self, h):
        return h - self.min[2]

    def getLocalCoords(self, p):
        plh = p.getPLH()
        x = self.x(plh[0,0])
        y = self.y(plh[1,0])
        z = self.z(plh[2,0])
        loc = np.array([x,y,z])

        if isinstance(p, point.Point):
            return point.Point(id=p.id, code=p.code, coord=loc)
        elif isinstance(p, station.Station):
            return station.Station(id=p.id, code=p.code, coord=loc)
