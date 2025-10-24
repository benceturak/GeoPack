import numpy as np
import point


class Station(point.Point):

    def __init__(self, id='', code='', coord=np.array([[0.0],[0.0],[0.0]]), type=point.XYZ, system=None):
        super(Station, self).__init__(id = id, code = code, coord = coord, type = type, system = system)
        self.troposphere = None

    #def addTropo(self, tropo):
    #
    #    if isinstance(tropo, TropoStation):
    #        self.troposphere = tropo
    #    else:
    #        raise TypeError()

    def __sub__(self, other):
        if not isinstance(other, point.Point):
            raise TypeError("other must be Point type")
        return Station(id=self._id, code=self.code, coord=(self.xyz - other.xyz), system=self.system)
    
    def __add__(self, other):
        if not isinstance(other, point.Point):
            raise TypeError("other must be Point type")
        return Station(id=self._id, code=self.code, coord=(self.xyz + other.xyz), system=self.system)



    #def __repr__(self):
        #return 0#self.coord
