import numpy as np

class Network(object):
    """Network class to collect stations and satellites.

    """
    def __init__(self):
        """Network constructor

        """
        self.stations = []
        self.satellites = []

    def getStations(self):
        """get stations method
            :return: all of stations (Point object), generator
        """
        for s in self.stations:
            yield s
    def getSatellites(self):
        """get satellites method
            :return: all of satellites (Satellite object), generator
        """
        for s in self.satellites:
            yield s
    def getStationBy4digitId(self, id):
        """get an exect station, select by the 4 digit IDű
            :param id: 4 digit ID (Str)
            :return: station (Point)

        """
        for s in self.stations:
            if s.id == id:
                return s

    def addStation(self, st):
        """add station to the network
            :param st: station (Point)

        """
        self.stations.append(st)
    def addSatellite(self, sat):
        """add satellite to the network
            :param sat: satellite (Satellite)

        """
        self.satellites.append(sat)

    def getStationsMatrix(self):
        """get stations' ids and coordinates in matrix
            :return: ids and coordinates of stations (tuple {ids: (Str), coords: numpy array (n,3)})
        """
        mat = np.empty((0,3))
        ids = np.empty((0,1))
        for st in self.stations:
            mat = np.append(mat, st.getPLH().T, axis=0)
            ids = np.append(ids, st.id)

        res = {}
        res['ids'] = ids
        res['coords'] = mat

        return res
