

class ReferenceSystem(object):

    def __init__(self, ellipsoid=None):
        self.ellipsoid = ellipsoid

    def getXYZ(self, plh):
        return self.ellipsoid.getXYZ(plh)

    def getPLH(self, xyz):
        return self.ellipsoid.getPLH(xyz)

    def setEllpisoid(self, ellipsoid):pass


    def getTransformParams(self, RS):pass

    def transformTo(self, point, RS):pass



class ITRS(ReferenceSystem):
    pass

class ETRS(ReferenceSystem):
    pass

class WGS84System(ReferenceSystem):
    pass

class PZ_90(ReferenceSystem):
    pass
