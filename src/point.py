import numpy as np
from wgs84 import WGS84
XYZ = 1
PLH = 2
class Point(object):

    #def __new__(self, id='', coord=np.array([[0.0],[0.0],[0.0]]), type=XYZ, system=WGS84()):
        #print("A")
        #if type == XYZ:
        #    from pointxyz import PointXYZ
            #return PointXYZ(id, coord, system)
        #elif type == PLH:
        #    from pointplh import PointPLH
            #return PointXYZ(id, coord, system)


    def __init__(self, id='', coord=np.array([[0.0],[0.0],[0.0]]), type=XYZ, system=WGS84()):
        self.id = id
        self.coord = coord
        self.system = system

    def __repr__(self):
        return self.coord.__repr__()
    def __str__(self):
        return self.coord.__str__()
