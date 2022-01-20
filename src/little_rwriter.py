import numpy as np

class Little_RWriter(object):

    def __init__(self):
        pass

    def header(self, lat=-888888, lon=-888888, id='', name='', platform='', source='', elevation=-888888, valid_fields=0, errors=0, warnings=0, seq_num=0, duplicates=0, sounding='F', bogus='F', discard='F', unix_time=-888888, julian_day=-888888, date='', sea_level_pressure=np.array([-888888,0]), reference_pressure=np.array([-888888,0]), ground_temperature=np.array([-888888,0]), sea_surface_temperature=np.array([-888888,0]), surface_pressure=np.array([-888888,0]), precipitation=np.array([-888888,0]), max_temperature=np.array([-888888,0]), min_temperature=np.array([-888888,0]), min_night_temperature=np.array([-888888,0]), pressure_tendancy_3H=np.array([-888888,0]), pressure_tendancy_24H=np.array([-888888,0]), cloud_cover=np.array([-888888,0]), ceiling=np.array([-888888,0]), PWpZTD=np.array([-888888,0])):
        header = "{:20.5f}{:20.5f}{:>40}{:>40}{:>40}{:>40}{:20.5f}{:10d}{:10d}{:10d}{:10d}{:10d}{:>10}{:>10}{:>10}{:10d}{:10d}{:>20}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"

        return header.format(lat, lon, id, name, platform, source, elevation, valid_fields, errors, warnings, seq_num, duplicates, sounding, bogus, discard, unix_time, julian_day, date, sea_level_pressure[0], sea_level_pressure[1], reference_pressure[0], reference_pressure[1], ground_temperature[0], ground_temperature[1], sea_surface_temperature[0], sea_surface_temperature[1], surface_pressure[0], surface_pressure[1], precipitation[0], precipitation[1], max_temperature[0], max_temperature[1], min_temperature[0], min_temperature[1], min_night_temperature[0], min_night_temperature[1], pressure_tendancy_3H[0], pressure_tendancy_3H[1], pressure_tendancy_24H[0], pressure_tendancy_24H[1], cloud_cover[0], cloud_cover[1], ceiling[0], ceiling[1], PWpZTD[0], PWpZTD[1])
    def data(self, P=np.array([-888888, 0]), H=np.array([-888888, 0]), T=np.array([-888888, 0]), Td=np.array([-888888, 0]), Sp=np.array([-888888, 0]), Dr=np.array([-888888, 0]), U=np.array([-888888, 0]), V=np.array([-888888, 0]), RH=np.array([-888888, 0]), Th=np.array([-888888, 0])):
        data = "{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}{:13.5f}{:7d}"

        return data.format(P[0], P[1], H[0], H[1], T[0], T[1], Td[0], Td[1], Sp[0], Sp[1], Dr[0], Dr[1], U[0], U[1], V[0], V[1], RH[0], RH[1], Th[0], Th[1])
    def end(self):

        return self.data(P=np.array([-777777, 0]), H=np.array([-777777, 0]))

    def tail(self, valid_fields=0, errors=0, warnings=0):
        tail = "{:7d}{:7d}{:7d}"

        return tail.format(valid_fields, errors, warnings)

    def write(self):
        pass

if __name__ == "__main__":

    writer = Little_RWriter()

    #print("{:>5}".format('a'))
    print(writer.header(id='aaaaaa', name='bbbbbbbb', platform='cccccccccccccccc', source='dddddddddddddddddd', date='20220120193500'))

    print(writer.data())
    print(writer.end())
