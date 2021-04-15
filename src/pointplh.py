import point
from wgs84 import WGS84
import numpy as np

class PointPLH(point.Point):

    def __init__(self, id='', coord=np.array([[0.0],[0.0],[0.0]]), system=WGS84()):

        super(PointPLH, self).__init__(id = id, coord = coord, type = point.PLH, system = system)

    def getXYZ(self):
        from pointxyz import PointXYZ
        return PointXYZ(self.id, self.system.getXYZ(self), self.system)

    @property
    def p(self):
        return self.coord[0]
    @property
    def l(self):
        return self.coord[1]
    @property
    def h(self):
        return self.coord[2]
