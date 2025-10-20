import numpy as np
import ellipsoid
XYZ = 1
PLH = 2
class Point(object):
    """!Point class to store and make calculations on points in cartesian and geographical coordinate system
        
    """


    def __init__(self, id='', code='', coord=np.array([[0.0],[0.0],[0.0]]), type=XYZ, system=None, other=None):
        """!Point inizializer
        @param id (str): point ID, default: ''
        @param code (str): point coode (Str), default: ''
        @param coord (numpy array (3,1)): coordinates (cartesian or geographical), default: [[0, 0, 0]]
        @param type (int): type of coordinate system, variable: XYZ/PLH , default: XYZ
        @param system (Ellipsoid object): base ellipsoid, default: None

        """
        if not isinstance(id, str):
            raise TypeError("id must be String!")
        if np.shape(coord) != (3, 1) and np.shape(coord) != (1, 3) and np.shape(coord) != (3,):
            raise TypeError("coord must be 3x1 numpy matrix!")
        if not isinstance(type, int):
            raise TypeError("type must be integer!")
        if not isinstance(system, ellipsoid.Ellipsoid) and system != None:
            raise TypeError("system must Ellipoid or None type!")

        self._id = id
        self.code = code

        if type == XYZ:
            if np.shape(coord) == (3, 1):
                self._xyz = coord
            elif np.shape(coord) == (1, 3):
                self._xyz = coord.T
            elif np.shape(coord) == (3,):
                self._xyz = np.array([coord]).T
            self._plh = None
        elif type == PLH:
            self._xyz = None
            if np.shape(coord) == (3, 1):
                self._plh = coord
            elif np.shape(coord) == (1, 3):
                self._plh = coord.T
            elif np.shape(coord) == (3,):
                self._plh = np.array([coord]).T

        else:
            raise TypeError()


        self.system = system
        self._other = other
    def getXYZ(self):
        """!get coordinates in cartesian system. For the transformation to set up system is required
        @return coord: cartesian coordinates (numpy array (3,1))
        """
        if np.shape(self._xyz) != (3, 1):
            if self.system != None:
                self._xyz = self.system.getXYZ(self._plh)
            else:
                raise TypeError("must be set up system to calculate the XYZ coords!")
        return self._xyz

    def getPLH(self):
        """get coordinates in ellipsoidal system. For the transformation to set up system is required
        @return coord: ellipsoidal coordinates (numpy array (3,1))
        """
        if np.shape(self._plh) != (3, 1):

            if self.system != None:
                self._plh = self.system.getPLH(self._xyz)
            else:
                raise TypeError("must be set up system to calculate the phi, lambda, h coords!")
        return self._plh

    @property
    def xyz(self):
        if np.shape(self._xyz) == (3, 1):
            return self._xyz
        else:
            return self.getXYZ()
    @xyz.setter
    def xyz(self, c):
        self._xyz = c
    @property
    def plh(self):
        if np.shape(self._plh) == (3, 1):
            return self._plh
        else:
            return self.getPLH()
    @plh.setter
    def plh(self, c):
        self._plh = c

    @property
    def id(self):
        return self._id

    @property
    def other(self):
        return self._other

    def dist(self, other):
        """!get distance from another Point
        @param other: point (Point object)
        @return: distance between the two points (float)
        """
        if isinstance(other, Point):
            xyz1 = self.getXYZ()
            xyz2 = other.getXYZ()
            return np.sqrt((xyz1[0,0] - xyz2[0,0])**2 + (xyz1[1,0] - xyz2[1,0])**2 + (xyz1[2,0] - xyz2[2,0])**2)
        else:
            raise TypeError()




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
