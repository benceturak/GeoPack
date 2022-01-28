import numpy as np
from epoch import Epoch

class Little_RWriter(object):

    def __init__(self, fname):
        self.fname = fname
        self._stations =[]


    def addStation(self, station):
        self._stations.append(station)

    def header(self, lat=-888888, lon=-888888, id='', name='', platform='', source='', elevation=-888888, valid_fields=0, errors=0, warnings=0, seq_num=0, duplicates=0, sounding='F', bogus='F', discard='F', unix_time=-888888, julian_day=-888888, date='', sea_level_pressure=np.array([-888888,0]), reference_pressure=np.array([-888888,0]), ground_temperature=np.array([-888888,0]), sea_surface_temperature=np.array([-888888,0]), surface_pressure=np.array([-888888,0]), precipitation=np.array([-888888,0]), max_temperature=np.array([-888888,0]), min_temperature=np.array([-888888,0]), min_night_temperature=np.array([-888888,0]), pressure_tendancy_3H=np.array([-888888,0]), pressure_tendancy_24H=np.array([-888888,0]), cloud_cover=np.array([-888888,0]), ceiling=np.array([-888888,0]), PWpZTD=np.array([-888888,0])):
        header = "{:20.5f}{:20.5f}{:>40}{:>40}{:>40}{:>40}{:20.5f}{:10d}{:10d}{:10d}{:10d}{:10d}{:>10}{:>10}{:>10}{:10d}{:10d}{:>20}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"

        return header.format(lat, lon, id, name, platform, source, elevation, valid_fields, errors, warnings, seq_num, duplicates, sounding, bogus, discard, unix_time, julian_day, date, sea_level_pressure[0], int(sea_level_pressure[1]), reference_pressure[0], int(reference_pressure[1]), ground_temperature[0], int(ground_temperature[1]), sea_surface_temperature[0], int(sea_surface_temperature[1]), surface_pressure[0], int(surface_pressure[1]), precipitation[0], int(precipitation[1]), max_temperature[0], int(max_temperature[1]), min_temperature[0], int(min_temperature[1]), min_night_temperature[0], int(min_night_temperature[1]), pressure_tendancy_3H[0], int(pressure_tendancy_3H[1]), pressure_tendancy_24H[0], int(pressure_tendancy_24H[1]), cloud_cover[0], int(cloud_cover[1]), ceiling[0], int(ceiling[1]), PWpZTD[0], int(PWpZTD[1]))


        return tail.format(valid_fields, errors, warnings)

    def data(self, P=np.array([-888888, 0]), H=np.array([-888888, 0]), T=np.array([-888888, 0]), Td=np.array([-888888, 0]), Sp=np.array([-888888, 0]), Dr=np.array([-888888, 0]), U=np.array([-888888, 0]), V=np.array([-888888, 0]), RH=np.array([-888888, 0]), Th=np.array([-888888, 0])):
        data = "{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"

        return data.format(P[0], P[1], H[0], H[1], T[0], T[1], Td[0], Td[1], Sp[0], Sp[1], Dr[0], Dr[1], U[0], U[1], V[0], V[1], RH[0], RH[1], Th[0], Th[1])
    def end(self):

        return self.data(P=np.array([-777777, 0]), H=np.array([-777777, 0]))

    def tail(self, valid_fields=0, errors=0, warnings=0):
        tail = "{:7d}{:7d}{:7d}"

        return tail.format(valid_fields, errors, warnings)

    def write(self):

        with open(self.fname, 'x') as fid:

            for s in self._stations:
                if s._src == 'FM-114':

                    print(self.header(lat=s.lat, lon=s.lon, id=s.id, source=s.source, PWpZTD=s.ztd), file=fid)

                    print(self.data(), file=fid)
                    print(self.end(), file=fid)
                    print(self.tail(valid_fields=1), file=fid)
                else:
                    pass

                    fid.close()



class Little_RStation(object):
    source_list = {'FM-114': 'GPSZD'}

    def __init__(self, lat, lon, alt, id, epoch, source='FM-114'):

        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.id = id
        self.epoch = epoch

        self._src = source

        self._data = np.empty((0,10))
        self._QC = np.empty((0,10))

        print(self._src)

    @property
    def source(self):
        return self._src + " " + self.source_list[self._src]

    def setZTD(self, ztd):
        self.ztd = ztd


    def add_data(self, data=np.array([[-888888, -888888, -888888, -888888, -888888, -888888, -888888, -888888, -888888, -888888]]), QC=np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])):pass




if __name__ == "__main__":

    sta = Little_RStation(lat=41, lon=19, alt=120.5, id='aaa', epoch=Epoch(np.array([2022,1,28,16,5,0])))

    sta.setZTD(np.array([0.145, 0]))

    writer = Little_RWriter('pppppp.obs')

    writer.addStation(sta)

    writer.write()

    #print("{:>5}".format('a'))
    #print(writer.header(id='aaaaaa', name='bbbbbbbb', platform='cccccccccccccccc', source='dddddddddddddddddd', date='20220120193500'))

    #print(writer.data())
    #print(writer.end())
