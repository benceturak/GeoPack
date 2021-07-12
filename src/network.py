import numpy as np

class Network(object):

    def __init__(self):
        self.stations = []
        self.satellites = []

    def getStations(self):
        for s in self.stations:
            yield s
    def getSatellites(self):
        for s in self.satellites:
            yield s

    def addStation(self, st):
        self.stations.append(st)
    def addSatellite(self, sat):
        self.satellites.append(sat)

    def getStationsMatrix(self):
        mat = np.empty((0,3))
        ids = np.empty((0,1))
        for st in self.stations:
            mat = np.append(mat, st.getPLH().T, axis=0)
            ids = np.append(ids, st.id)

        res = {}
        res['ids'] = ids
        res['coords'] = mat

        return res
