import numpy as np
import point
from epoch import Epoch
import ellipsoid
from scipy import interpolate

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

    def _getTimeframeStatementMax(self, ep_max):

        middle_days_st = " (DATE<'"+ ep_max.date()+"')"

        last_day_st = " (DATE='"+ep_max.date() + "' AND TIME<='"+ep_max.time()+"')"

        return " (" + middle_days_st + " OR" + last_day_st + ")"



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

    def getRAOBSNwAtep(self, station_id, ep):

        sql = "SELECT HEIGHT, N_WET FROM RAOBSREFR WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"' AND WMOID="+ str(station_id) +" ORDER BY HEIGHT ASC"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,2))
        for s in dbcursor.fetchall():

            res = np.append(res, [[s[0], s[1]]], axis=0)

        return res

    def getRAOBSTempAtep(self, station_id, ep):

        sql = "SELECT HEIGHT, TEMPERATURE FROM RAOBSREFR WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"' AND WMOID="+ str(station_id) +" ORDER BY HEIGHT ASC"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,2))
        for s in dbcursor.fetchall():

            res = np.append(res, [[s[0], s[1]]], axis=0)

        return res

    def getRAOBSPressAtep(self, station_id, ep):

        sql = "SELECT HEIGHT, PRESSURE FROM RAOBSREFR WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"' AND WMOID="+ str(station_id) +" ORDER BY HEIGHT ASC"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,2))
        for s in dbcursor.fetchall():

            res = np.append(res, [[s[0], s[1]]], axis=0)

        return res
    
    def getRAOBSNdryAtep(self, station_id, ep):

        sql = "SELECT HEIGHT, N_DRY FROM RAOBSREFR WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"' AND WMOID="+ str(station_id) +" ORDER BY HEIGHT ASC"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,2))
        for s in dbcursor.fetchall():

            res = np.append(res, [[s[0], s[1]]], axis=0)

        return res

    def getRAOBSNwetAtep(self, station_id, ep):

        sql = "SELECT HEIGHT, N_WET FROM RAOBSREFR WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"' AND WMOID="+ str(station_id) +" ORDER BY HEIGHT ASC"

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,2))
        for s in dbcursor.fetchall():

            res = np.append(res, [[s[0], s[1]]], axis=0)

        return res

    def getLastRAOBSep(self, station_id, to=None):
        if to is None:
            sql = "SELECT DATE, TIME FROM RAOBSREFR WHERE WMOID="+station_id+" ORDER BY `DATE` DESC, `TIME` DESC LIMIT 1;"

            dbcursor = self._database.cursor()

            dbcursor.execute(sql)

            res = np.empty((0,2))
            for s in dbcursor.fetchall():
                

                date = str(s[0]).split("-")
                time = str(s[1]).split(":")

                return Epoch(np.array([s[0].year, s[0].month, s[0].day, int(time[0]), int(time[1]), int(time[2])]))

            return False
        else:
            sql = "SELECT DATE, TIME FROM RAOBSREFR WHERE WMOID="+station_id+" AND " + self._getTimeframeStatementMax(to) + " ORDER BY `DATE` DESC, `TIME` DESC LIMIT 1;"

            dbcursor = self._database.cursor()

            dbcursor.execute(sql)

            res = np.empty((0,2))
            for s in dbcursor.fetchall():
                

                date = str(s[0]).split("-")
                time = str(s[1]).split(":")

                return Epoch(np.array([s[0].year, s[0].month, s[0].day, int(time[0]), int(time[1]), int(time[2])]))

            return False






    def chechAvailabilityTrpDelay(self, stations=None, fr=None, to=None):

        sql = 'SELECT STATION, DATE, TIME FROM TRPDELAY WHERE CONSTELLATION=0 AND ' + self._getStationsStatement(stations) + ' AND' + self._getTimeframeStatement(fr, to)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,3))
        for s in dbcursor.fetchall():
            time = s[2].__str__().split(':')
            ep = Epoch(np.array([s[1].year, s[1].month, s[1].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[s[0], ep, s[3]]], axis=0)

        return res


    def getNw(self, lat=(), lon=(), alt=(), fr=None, to=None):


        sql = 'SELECT DATE, TIME, LAT, LON, ALT, NW FROM 3DREFRACTIVITY_W WHERE ' + self._getTimeframeStatement(fr, to) + ' AND ' + self._getLocationLatStatement(lat) + ' AND ' + self._getLocationLonStatement(lon) + ' AND ' + self._getLocationAltStatement(alt)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,5))

        for s in dbcursor.fetchall():
            time = s[1].__str__().split(':')
            ep = Epoch(np.array([s[0].year, s[0].month, s[0].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[ep, s[2], s[3], s[4], s[5]]], axis=0)

        return res

    def getNwAtEp(self, ep):

        sql = "SELECT DATE, TIME, LAT, LON, ALT, NW FROM 3DREFRACTIVITY_W WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"'"
        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,5))

        x = np.empty((0,))
        y = np.empty((0,))
        z = np.empty((0,))

        Nw_rows = np.empty((0,4))

        for s in dbcursor.fetchall():
            if not s[2] in x:
                x = np.append(x, s[2])
            if not s[3] in y:
                y = np.append(y, s[3])
            if not s[4] in z:
                z = np.append(z, s[4])
            Nw_rows = np.append(Nw_rows, [[s[2], s[3], s[4], s[5]]], axis=0)
        np.sort(x)
        np.sort(y)
        np.sort(z)


        Nw = np.empty((len(x),len(y),len(z)))

        for xv in x:
            for yv in y:
                for zv in z:
                    i = np.all(np.array([Nw_rows[:,0] == xv, Nw_rows[:,1] == yv, Nw_rows[:,2] == zv]), axis=0)
                    Nw[np.where(x == xv)[0], np.where(y == yv)[0], np.where(z == zv)[0]] = Nw_rows[i,3]

        return (Nw, x, y, z)

    def getNw(self, lat=(), lon=(), alt=(), fr=None, to=None):


        sql = 'SELECT DATE, TIME, LAT, LON, ALT, WVDENSITY FROM 3DWVDENSITY ' + self._getTimeframeStatement(fr, to) + ' AND ' + self._getLocationLatStatement(lat) + ' AND ' + self._getLocationLonStatement(lon) + ' AND ' + self._getLocationAltStatement(alt)

        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,5))

        for s in dbcursor.fetchall():
            time = s[1].__str__().split(':')
            ep = Epoch(np.array([s[0].year, s[0].month, s[0].day, int(time[0]), int(time[1]), int(time[2])]))
            res = np.append(res, [[ep, s[2], s[3], s[4], s[5]]], axis=0)

        return res

    def getWVDAtEp(self, ep):

        sql = "SELECT DATE, TIME, LAT, LON, ALT, WVDENSITY FROM 3DWVDENSITY WHERE DATE='"+ep.date()+"' AND TIME='"+ep.time()+"'"
        dbcursor = self._database.cursor()

        dbcursor.execute(sql)

        res = np.empty((0,5))

        x = np.empty((0,))
        y = np.empty((0,))
        z = np.empty((0,))

        Nw_rows = np.empty((0,4))

        for s in dbcursor.fetchall():
            if not s[2] in x:
                x = np.append(x, s[2])
            if not s[3] in y:
                y = np.append(y, s[3])
            if not s[4] in z:
                z = np.append(z, s[4])
            Nw_rows = np.append(Nw_rows, [[s[2], s[3], s[4], s[5]]], axis=0)
        np.sort(x)
        np.sort(y)
        np.sort(z)


        Nw = np.empty((len(x),len(y),len(z)))

        for xv in x:
            for yv in y:
                for zv in z:
                    i = np.all(np.array([Nw_rows[:,0] == xv, Nw_rows[:,1] == yv, Nw_rows[:,2] == zv]), axis=0)
                    Nw[np.where(x == xv)[0], np.where(y == yv)[0], np.where(z == zv)[0]] = Nw_rows[i,3]

        return (Nw, x, y, z)

    def getProfile(self, data, x, y, z, lat, lon, kind):
        profile = np.empty((0,2))

        for i in range(0,np.shape(data)[2]):
            f_Nw = interpolate.interp2d(x,y, data[:,:,i].T, kind=kind)
            profile =  np.append(profile,[[z[i],f_Nw(lat, lon)[0]]], axis=0)

        return profile




    def getNwProfile(self, lat, lon, ep, kind='linear'):
        Nw, x, y, z = self.getNwAtEp(ep)

        return self.getProfile(Nw, x, y, z, lat, lon, kind)

    def getWVDProfile(self, lat, lon, ep, kind='linear'):
        WVD, x, y, z = self.getWVDAtEp(ep)

        return self.getProfile(WVD, x, y, z, lat, lon, kind)





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

    def getZHD(self, stations=None, fr=None, to=None):


        sql = 'SELECT STATION, DATE, TIME, ZHD FROM TRPDELAY WHERE CONSTELLATION=0 AND ' + self._getStationsStatement(stations) + ' AND' + self._getTimeframeStatement(fr, to)

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

    def getStationTypes(self):
        sql = "SELECT * FROM STATIONTYPE"
        dbcursor = self._database.cursor()
        dbcursor.execute(sql)

        res = {}

        for i in dbcursor.fetchall():
            res[str(i[0])] = i[1]

        return res


    def getStations(self, station_type=None):
        
        types = self.getStationTypes()
        if station_type == None:
            sql = "SELECT STATION, LAT, LON, HEIGHT, TYPE FROM STATION"
        else:
            sql = "SELECT STATION, LAT, LON, HEIGHT, TYPE FROM STATION WHERE TYPE="+str(list(types.keys())[list(types.values()).index(station_type)])
        dbcursor = self._database.cursor()
        dbcursor.execute(sql)

        for sta in dbcursor.fetchall():
            yield point.Point(id=sta[0], code=types[str(sta[4])], coord=np.array([sta[1], sta[2], sta[3]]), type=point.PLH, system=ellipsoid.WGS84())


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
    import sys
    sys.path.append("../apps/gpsmet_analysis")
    import dbconfig

    db = ReadDB(dbconfig.database)

    a = Epoch(np.array([2022,2,2,18,0,0]))
    b = Epoch(np.array([2022,1,1,8,5,0]))
    #getNwProfile(self, lat, lon, ep):
    for i in db.getStations():
        print(i.code)

    #db.getNwProfile(45,17,a,0)
    exit()
    print(db._getTimeframeStatement(a,b))

    print(db._getStationsStatement(('AAAA', 'BBBB', 'CCCC', 'DDDD')))
