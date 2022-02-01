import numpy as np
import point
from epoch import Epoch
import ellipsoid

class ReadDB(object):
    """
        ReadDB class to read gpsmet database

            :param db:
    """

    def __init__(self, database=None):
        self._database = database

    def _getStationsStatement(self, stations=None):
        """

        """

        if stations != None:
            str = ' STATION IN ('
            for s in stations:
                str = str + "'" + s + "',"

            str = str[0:-1] + ')'

            return str
        else:
            return "1"

    def _getTimeframeStatement(self, ep_min, ep_max):


        if ep_min.date() != ep_max.date():

            first_day_st = " (DATE='"+ep_min.date() + "' AND TIME>='"+ep_min.time()+"')"

            middle_days_st = " (DATE>'"+ ep_min.date() +"' AND DATE<'"+ ep_max.date()+"')"

            last_day_st = " (DATE='"+ep_max.date() + "' AND TIME<='"+ep_max.time()+"')"

            return " (" + first_day_st + " OR" + middle_days_st + " OR" + last_day_st + ")"
        else:
            return " (DATE='"+ep_min.date() + "' AND TIME>='"+ep_min.time()+"' AND TIME<='"+ep_max.time()+"')"



    def _getAllStations(self):

        sql = "SELECT * FROM STATION"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)
        return dbcursor.fetchall()

    def _getLocationLatStatement(self, lat):

        return '(LAT>=' + str(lat[0]) + ' AND LAT<= ' + str(lat[1]) + ')'

    def _getLocationLonStatement(self, lon):

        return '(LON>=' + str(lon[0]) + ' AND LON<=' + str(lon[1]) + ')'

    def _getLocationAltStatement(self, alt):

        return '(ALT>=' + str(alt[0]) + ' AND ALT<= ' + str(alt[1]) + ')'

    def getNw(self, lat=(), lon=(), alt=(), fr=None, to=None):


        sql = 'SELECT DATE, TIME, LAT, LON, ALT, NW FROM 3DREFRACTIVITY WHERE ' + self._getTimeframeStatement(fr, to) + ' AND ' + self._getLocationLatStatement(lat) + ' AND ' + self._getLocationLonStatement(lon) + ' AND ' + self._getLocationAltStatement(alt)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,5))

        for s in dbcursor.fetchall():
            time = s[1].__str__().split(':')
            ep = Epoch(np.array([s[0].year, s[0].month, s[0].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[ep, s[2], s[3], s[4], s[5]]], axis=0)

        return res
    def getZWD(self, stations=None, fr=None, to=None):


        sql = 'SELECT STATION, DATE, TIME, ZWD FROM TRPDELAY WHERE CONSTELLATION=0 AND ' + self._getStationsStatement(stations) + ' AND' + self._getTimeframeStatement(fr, to)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,3))
        for s in dbcursor.fetchall():
            time = s[2].__str__().split(':')
            ep = Epoch(np.array([s[1].year, s[1].month, s[1].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[s[0], ep, s[3]]], axis=0)

        return res

    def getZTD(self, stations=None, fr=None, to=None):


        sql = 'SELECT STATION, DATE, TIME, ZTD FROM TRPDELAY WHERE CONSTELLATION=0 AND ' + self._getStationsStatement(stations) + ' AND' + self._getTimeframeStatement(fr, to)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,3))
        for s in dbcursor.fetchall():
            time = s[2].__str__().split(':')
            ep = Epoch(np.array([s[1].year, s[1].month, s[1].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[s[0], ep, s[3]]], axis=0)

        return res

    def getStation(self, id4d):
        sql = "SELECT STATION, LAT, LON, HEIGHT FROM STATION WHERE STATION='" + id4d + "'"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = dbcursor.fetchall()

        if res == []:
            raise ValueError('Unknown station:' + id4d)
        res = res[0]
        return point.Point(id=res[0], coord=np.array([res[1], res[2], res[3]]), type=point.PLH, system=ellipsoid.WGS84())


if __name__ == "__main__":


    db = ReadDB('aaaa')

    a = Epoch(np.array([2022,1,1,2,21,0]))
    b = Epoch(np.array([2022,1,1,8,5,0]))

    print(db._getTimeframeStatement(a,b))

    print(db._getStationsStatement(('AAAA', 'BBBB', 'CCCC', 'DDDD')))
