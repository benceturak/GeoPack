import numpy as np
import point
from tropostation import TropoStation

class Station(point.Point):

    def __init__(self, id='', code='', coord=np.array([[0.0],[0.0],[0.0]]), type=point.XYZ, system=None):
        super(Station, self).__init__(id = id, code = code, coord = coord, type = type, system = system)
        self.troposphere = None

    def addTropo(self, tropo):

        if isinstance(tropo, TropoStation):
            self.troposphere = tropo
        else:
            raise TypeError()





    #def __repr__(self):
        #return 0#self.coord
