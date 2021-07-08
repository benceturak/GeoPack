import math
import numpy as np


class Rotation(object):

    def __init__(self, x=0, y=0, z=0, orther='xyz'):

        Rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
        Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
        Rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])

        if orther=='xyz':
            self.matrix = np.dot(np.dot(Rx,Ry), Rz)
        elif orther == 'xzy':
            self.matrix = np.dot(np.dot(Rx,Rz), Rx)
        elif orther == 'yxz':
            self.matrix = np.dot(np.dot(Ry,Rx), Rz)
        elif orther == 'yzx':
            self.matrix = np.dot(np.dot(Ry,Rz), Ry)
        elif orther == 'zxy':
            self.matrix = np.dot(np.dot(Rz,Rx), Ry)
        elif orther == 'zyx':
            self.matrix = np.dot(np.dot(Rz,Ry), Rx)

    def setRot(self, R):
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
