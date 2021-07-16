import numpy as np
import point

class Line(object):

    def __init__(self, p, alpha, e):

        xyz = p.getXYZ()
        self.x = lambda t: xyz[0,0] + t*np.sin(e)
        self.y = lambda t: xyz[1,0] + t*np.cos(alpha)
        self.z = lambda t: xyz[2,0] + t*np.sin(alpha)

        self.xr = lambda x: (x - xyz[0,0])/np.sin(e)
        self.yr = lambda y: (y - xyz[1,0])/np.cos(alpha)
        self.zr = lambda z: (z - xyz[2,0])/np.sin(alpha)

    def getPointAtT(self, t):
        for tt in t:
            yield point.Point(coord=np.array([self.x(tt),self.y(tt),self.z(tt)]))
    def getTwhereX(self, x):
        return self.xr(x)
    def getTwhereY(self, y):
        return self.yr(y)
    def getTwhereZ(self, z):
        return self.zr(z)
