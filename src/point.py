import numpy as np
from wgs84 import WGS84
from ellipsoid import Ellipsoid
XYZ = 1
PLH = 2
class Point(object):


    def __init__(self, id='', coord=np.array([[0.0],[0.0],[0.0]]), type=XYZ, system=None):
        if not isinstance(id, str):
            raise TypeError("id must be String!")
        if np.shape(coord) != (3, 1) and np.shape(coord) != (1, 3) and np.shape(coord) != (3,):
            raise TypeError("coord must be 3x1 numpy matrix!")
        if not isinstance(type, int):
            raise TypeError("type must be integer!")
        if not isinstance(system, Ellipsoid) and system != None:
            raise TypeError("system must Ellipoid or None type!")

        self.id = id

        if type == XYZ:
            if np.shape(coord) == (3, 1):
                self.xyz = coord
            elif np.shape(coord) == (1, 3):
                self.xyz = coord.T
            elif np.shape(coord) == (3,):
                self.xyz = np.array([coord]).T
            self.plh = None
        elif type == PLH:
            self.xyz = None
            if np.shape(coord) == (3, 1):
                self.plh = coord
            elif np.shape(coord) == (1, 3):
                self.plh = coord.T
            elif np.shape(coord) == (3,):
                self.plh = np.array([coord]).T

        else:
            raise TypeError()


        self.system = system
    def getXYZ(self):
        if np.shape(self.xyz) != (3, 1):
            if self.system != None:
                self.xyz = self.system.getXYZ(self.plh)
            else:
                raise TypeError("must be set up system to calculate the XYZ coords!")
        return self.xyz

    def getPLH(self):
        if np.shape(self.plh) != (3, 1):
            if self.system != None:
                self.plh = self.system.getPLH(self.xyz)
            else:
                raise TypeError("must be set up system to calculate the phi, lambda, h coords!")
        return self.plh

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("other must be Point type")
        return Point(coord=(self.xyz + other.xyz))
    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError("other must be Point type")
        return Point(coord=(self.xyz - other.xyz))
    def __repr__(self):
        return self.xyz.__repr__()
    def __str__(self):
        return self.xyz.__str__()

if __name__ == "__main__":

    p = Point(id='1', coord=np.array([1,2,3]))
