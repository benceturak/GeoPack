import numpy as np
from epoch import Epoch

class Little_RWriter(object):
    """Little_RWrtiter class to collect and write atmospheric data to LittleR formatted text file
        :param fname: name and location of the destination file (STR)

    """

    def __init__(self, fname):
        """Little_RWriter constructor

        """
        self.fname = fname
        self._stations =[]


    def addStation(self, station):
        """Add new station to the Little_R file
            :param station: real or virtual observation station ()

        """
        self._stations.append(station)

    def header(self, lat=-888888, lon=-888888, id='', name='', fm_code='', source='', elevation=-888888, valid_fields=0, errors=0, warnings=0, seq_num=0, duplicates=0, sounding='F', bogus='F', discard='F', unix_time=-888888, julian_day=-888888, date='', sea_level_pressure=np.array([-888888,0]), reference_pressure=np.array([-888888,0]), ground_temperature=np.array([-888888,0]), sea_surface_temperature=np.array([-888888,0]), surface_pressure=np.array([-888888,0]), precipitation=np.array([-888888,0]), max_temperature=np.array([-888888,0]), min_temperature=np.array([-888888,0]), min_night_temperature=np.array([-888888,0]), pressure_tendancy_3H=np.array([-888888,0]), pressure_tendancy_24H=np.array([-888888,0]), cloud_cover=np.array([-888888,0]), ceiling=np.array([-888888,0]), PWpZTD=np.array([-888888,0])):
        """Set and fomat header of stations
            For more information visit: https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html
            :param lat: latitude of station (float), default: -888888
            :param lon: longitude of station (float), default: -888888
            :param id: ID of station (Str), default: ""
            :param name: name of station (Str), default: ""
            :param fm_code: fm_code describes the type of observation (Str), default: ""
            :param source: sourca of observations (Str), default: ""
            :param elevation: elevation of ths station (float), default: -888888
            :param valid_fields: number of valid field in observation (int), default: -888888
            :param errors: number of reported errors in observation (int), default: -888888
            :param warnings: number of reported warnings in observation (int), default: -888888
            :param seq_num:  sequential order of this observation type/set (int), default: 0
            :param duplicates: number of duplicate observations (int), default: 0
            :param sounding: true if observation is a profile (Str T/F), default: "F"
            :param bogus: true if observation is a "bogus" (Str T/F), default: "F"
            :param discard: true if observation has to be discarded (Str T/F), default: "F"
            :param unix_time: unix time (int), default: -888888
            :param julian_day: Julian Day (int), default: -888888
            :param date: date (Str - YYYYMMDDhhmmss), default: ""
            :param sea_level_pressure: (numpy array (2,0)), default: [-888888, 0]
            :param reference_pressure: (numpy array (2,0)), default: [-888888, 0]
            :param ground_temperature: (numpy array (2,0)), default: [-888888, 0]
            :param sea_surface_temperature: (numpy array (2,0)), default: [-888888, 0]
            :param surface_pressure: (numpy array (2,0)), default: [-888888, 0]
            :param precipitation: (numpy array (2,0)), default: [-888888, 0]
            :param max_temperature: (numpy array (2,0)), default: [-888888, 0]
            :param min_temperature: (numpy array (2,0)), default: [-888888, 0]
            :param min_night_temperature: (numpy array (2,0)), default: [-888888, 0]
            :param pressure_tendancy_3H: (numpy array (2,0)), default: [-888888, 0]
            :param pressure_tendancy_24H: (numpy array (2,0)), default: [-888888, 0]
            :param cloud_cover: (numpy array (2,0)), default: [-888888, 0]
            :param ceiling:(numpy array (2,0)), default: [-888888, 0]
            :param PWpZTD: (numpy array (2,0)), default: [-888888, 0]

            :return: formatted header (Str)
        """

        header = "{:20.5f}{:20.5f}{:<40}{:<40}{:<40}{:<40}{:20.5f}{:10d}{:10d}{:10d}{:10d}{:10d}{:>10}{:>10}{:>10}{:10d}{:10d}{:>20}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"

        return header.format(lat, lon, id, name, fm_code, source, elevation, valid_fields, errors, warnings, seq_num, duplicates, sounding, bogus, discard, unix_time, julian_day, date, sea_level_pressure[0], int(sea_level_pressure[1]), reference_pressure[0], int(reference_pressure[1]), ground_temperature[0], int(ground_temperature[1]), sea_surface_temperature[0], int(sea_surface_temperature[1]), surface_pressure[0], int(surface_pressure[1]), precipitation[0], int(precipitation[1]), max_temperature[0], int(max_temperature[1]), min_temperature[0], int(min_temperature[1]), min_night_temperature[0], int(min_night_temperature[1]), pressure_tendancy_3H[0], int(pressure_tendancy_3H[1]), pressure_tendancy_24H[0], int(pressure_tendancy_24H[1]), cloud_cover[0], int(cloud_cover[1]), ceiling[0], int(ceiling[1]), PWpZTD[0], int(PWpZTD[1]))


        return tail.format(valid_fields, errors, warnings)

    def data(self, P=np.array([-888888, 0]), H=np.array([-888888, 0]), T=np.array([-888888, 0]), Td=np.array([-888888, 0]), Sp=np.array([-888888, 0]), Dr=np.array([-888888, 0]), U=np.array([-888888, 0]), V=np.array([-888888, 0]), RH=np.array([-888888, 0]), Th=np.array([-888888, 0])):
        """Set and format data row
            For more information visit: https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html
            :param P: pressure (numpy array (2,0)), default: [-888888, 0]
            :param H: height (numpy array (2,0)), default: [-888888, 0]
            :param T: temperature (numpy array (2,0)), default: [-888888, 0]
            :param Td: dew point (numpy array (2,0)), default: [-888888, 0]
            :param Sp: wind speed (numpy array (2,0)), default: [-888888, 0]
            :param Dr: wind directions (numpy array (2,0)), default: [-888888, 0]
            :param U: East-West wind (numpy array (2,0)), default: [-888888, 0]
            :param V: North-South wind (numpy array (2,0)), default: [-888888, 0]
            :param Rh: relative humidity (numpy array (2,0)), default: [-888888, 0]
            :param Th: thickness (numpy array (2,0)), default: [-888888, 0]

            :return: formatted data row
        """
        data = "{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"
        return data.format(P[0], int(P[1]), H[0], int(H[1]), T[0], int(T[1]), Td[0], int(Td[1]), Sp[0], int(Sp[1]), Dr[0], int(Dr[1]), U[0], int(U[1]), V[0], int(V[1]), RH[0], int(RH[1]), Th[0], int(Th[1]))
    def end(self):
        """Set and format end row

            :return: formatted end row
        """

        return self.data(P=np.array([-777777, 0]), H=np.array([-777777, 0]))

    def tail(self, valid_fields=0, errors=0, warnings=0):
        """Set and format tail integer row
            :param valid_fields: number of valid fields of observation (int), default: 0
            :param erros: number of errors (int), default: 0
            :param warnings: number of warnings (int), default: 0

            :return: formatted tail row
        """
        tail = "{:7d}{:7d}{:7d}"

        return tail.format(valid_fields, errors, warnings)

    def write(self):
        """write observation data to text file

        """

        with open(self.fname, 'x') as fid:
            for s in self._stations:
                if s._fm_code == 'FM-114':
                    date = "{:4d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(s.epoch.dt[0], s.epoch.dt[1], s.epoch.dt[2], s.epoch.dt[3], s.epoch.dt[4], s.epoch.dt[5])  #str(s.epoch.dt[0]) + str(s.epoch.dt[1]) + str(s.epoch.dt[2]) + str(s.epoch.dt[3]) + str(s.epoch.dt[4]) + str(s.epoch.dt[5])
                    print(self.header(lat=s.lat, lon=s.lon, id=s.id, name=s.name, fm_code=s.fm_code, source=s.source, date=date, PWpZTD=np.array([s.ztd, 0])), file=fid)

                    print(self.data(), file=fid)
                    print(self.end(), file=fid)
                    print(self.tail(valid_fields=0), file=fid)

                elif s._fm_code == 'FM-116':
                    date = "{:4d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(s.epoch.dt[0], s.epoch.dt[1], s.epoch.dt[2], s.epoch.dt[3], s.epoch.dt[4], s.epoch.dt[5])
                    print(self.header(lat=s.lat, lon=s.lon, fm_code=s.fm_code, source=s.source, date=date), file=fid)
                    valid_fields = 0
                    for d in s.data:
                        print(self.data(P=d['P'], H=d['H'], T=d['T'], Td=d['Td']), file=fid)
                        valid_fields += 4
                    print(self.end(), file=fid)
                    print(self.tail(valid_fields=valid_fields), file=fid)

                else:
                    pass

                    fid.close()



class Little_RStation(object):
    """Little_RStation class to collect and store observation data station by station
        :param lat: latitude of station (float)
        :param lon: longitude of station (float)
        :param alt: altitude of station (float)
        :param id: id station (Str)
        :param name: name of station (Str)
        :param epoch: epoch of observation (Epoch object)
        :param source: source of observation (Str)
        :param fm-code: type of observation (Str)

    """
    fm_code_list = {'FM-114': 'GPSZTD', 'FM-116': 'GPSRF'}

    def __init__(self, lat=-888888, lon=-888888, alt=-888888, id='', name='', epoch='', source='', fm_code='FM-114'):
        """Little_RStation constructor

        """

        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.id = id
        self.name = name
        self.epoch = epoch
        self.source = source

        self._fm_code = fm_code

        self._data = []


    @property
    def fm_code(self):
        return self._fm_code + " " + self.fm_code_list[self._fm_code]

    def setZTD(self, ztd):
        self.ztd = ztd


    def add_data(self, P=np.array([-888888, 0]), H=np.array([-888888, 0]), T=np.array([-888888, 0]), Td=np.array([-888888, 0]), Sp=np.array([-888888, 0]), Dr=np.array([-888888, 0]), U=np.array([-888888, 0]), V=np.array([-888888, 0]), RH=np.array([-888888, 0]), Th=np.array([-888888, 0])):
        
        
        self._data.append({'P': P, 'H': H, 'T': T, 'Td': Td, 'Sp': Sp, 'Dr': Dr, 'U': U, 'V': V, 'RH': RH, 'Th': Th})
    @property
    def data(self):
        for d in self._data:
            yield d




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
