import math
import numpy as np


class Rotation(object):
    """!Rotation class to transform points from a CRD to another 
    
    """
    def __init__(self, x=0, y=0, z=0, order='xyz'):
        """Rotation initializer
        @param x (float): rotation angle around axis x in radian, default: 0
        @param y (float): rotation angle around axis y in radian, default: 0
        @param z (float): rotation angle around axis z in radian, default: 0
        @param order (str): order of rotations' axis, default: 'xyz'

        """
        Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
        Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
        Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])

        if order=='xyz':
            self.matrix = np.dot(np.dot(Rx,Ry), Rz)
        elif order == 'xzy':
            self.matrix = np.dot(np.dot(Rx,Rz), Rx)
        elif order == 'yxz':
            self.matrix = np.dot(np.dot(Ry,Rx), Rz)
        elif order == 'yzx':
            self.matrix = np.dot(np.dot(Ry,Rz), Ry)
        elif order == 'zxy':
            self.matrix = np.dot(np.dot(Rz,Rx), Ry)
        elif order == 'zyx':
            self.matrix = np.dot(np.dot(Rz,Ry), Rx)

    def setRot(self, R):
        """!set up rotation matrix directly
        @param R (numpy array (3,3)): rotation matrix
        
        """
        self.matrix = R

    def __mul__(self, other):
        from point import Point
        if isinstance(other, Rotation):
            R = Rotation()
            R.setRot(np.dot(self.matrix, other.matrix))
            return R
        elif isinstance(other, Point) :
            return Point(id=other.id, coord=np.dot(self.matrix, other.xyz))
        elif isinstance(other,np.ndarray):
            ps = np.empty((0,))
            for p in other:
                ps = np.append(ps, Point(id=p.id, coord=(self*p).coord))
            return ps
        else:
            print(type(other))

    def __repr__(self):
        return self.matrix.__repr__()

    def __str__(self):
        return self.matrix.__str__()
