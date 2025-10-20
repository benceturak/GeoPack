import numpy as np
import point


class Station(point.Point):
    """!Station class to store and make calculations on points in cartesian and geographical coordinate system
        
    """
    def __init__(self, id='', code='', coord=np.array([[0.0],[0.0],[0.0]]), type=point.XYZ, system=None):
        """!Station initializer
        @param id (str): point ID, default: ''
        @param code (str): point coode (Str), default: ''
        @param coord (numpy array (3,1)): coordinates (cartesian or geographical), default: [[0, 0, 0]]
        @param type (int): type of coordinate system, variable: XYZ/PLH , default: XYZ
        @param system (Ellipsoid object): base ellipsoid, default: None
        """
        super(Station, self).__init__(id = id, code = code, coord = coord, type = type, system = system)
        self.troposphere = None

    #def addTropo(self, tropo):
    #
    #    if isinstance(tropo, TropoStation):
    #        self.troposphere = tropo
    #    else:
    #        raise TypeError()





    #def __repr__(self):
        #return 0#self.coord
