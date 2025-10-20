import numpy as np

class Network(object):
    """!Network class to collect stations and satellites.

    """
    def __init__(self):
        """!Network initializer

        """
        self.stations = []
        self.satellites = []

    def getStations(self):
        """!get stations method generator function
        @return network_stations (Station/Point): list of stations, generator
        """
        for s in self.stations:
            yield s
    def getSatellites(self):
        """!get satellites method generator function
        @return network_satellites (Satellite): list of satellites, generator
        """
        for s in self.satellites:
            yield s
    def getStationBy4digitId(self, id):
        """!get an exact station, select by the 4 digit ID
        @param id (str): 4 digit ID
        @return station (Station, Point): station

        """
        for s in self.stations:
            if s.id == id:
                return s

    def addStation(self, st):
        """!add station to the network
        @param st (Point,Station): station

        """
        self.stations.append(st)
    def addSatellite(self, sat):
        """!add satellite to the network
        @param sat (Satellite): satellite

        """
        self.satellites.append(sat)

    def getStationsMatrix(self):
        """!get stations' ids and coordinates in matrix
        @return (tuple {ids: (Str), coords: numpy array (n,3)}): ids and coordinates of stations 
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
