import point
from wgs84 import WGS84
import numpy as np

class PointXYZ(point.Point):

    def __init__(self, id='', coord=np.array([[0.0],[0.0],[0.0]]), system=WGS84()):

        super(PointXYZ, self).__init__(id = id, coord = coord, type = point.XYZ, system = system)


    def getPLH(self):
        from pointplh import PointPLH
        return PointPLH(self.id, self.system.getPLH(self), self.system)

    @property
    def x(self):
        return self.coord[0]
    @property
    def y(self):
        return self.coord[1]
    @property
    def z(self):
        return self.coord[2]
