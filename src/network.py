import numpy as np

class Network(object):

    def __init__(self):
        self.stations = []

    def addStation(self, st):
        self.stations.append(st)

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
