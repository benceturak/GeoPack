import numpy as np

from epoch import Epoch

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
            str = ' STATION=('
            for s in stations:
                str = str + s + ','

            str = str[0:-1] + ')'

            return str
        else:
            return ""

    def _getTimeframeStatement(self, ep_min, ep_max):


        if ep_min.date() != ep_max.date():

            first_day_st = " (DATE="+ep_min.date() + " AND TIME>="+ep_min.time()+")"

            middle_days_st = " (DATE>"+ ep_min.date() +" AND DATE<"+ ep_max.date()+")"

            last_day_st = " (DATE="+ep_max.date() + " AND TIME<="+ep_max.time()+")"

            return "(" + first_day_st + " OR" + middle_days_st + " OR" + last_day_st + ")"
        else:
            return "(DATE="+ep_min.date() + " AND TIME>="+ep_min.time()+" TIME<="+ep_max.time()+")"




    def getNw(self):
        pass

    def getZWD(self, stations=None, fr=None, to=None):

        stations_statement = self._getStationsStatement(satations)


        sql = 'SELECT STATION, DATE, TIME, ZWD WHERE CONSTELLATION=0 AND '+ self._getStationsStatement(satations) + 'AND' + self._getTimeframeStatement(fr, to)




if __name__ == "__main__":


    db = ReadDB('aaaa')

    a = Epoch(np.array([2022,1,1,2,21,0]))
    b = Epoch(np.array([2022,1,1,8,5,0]))

    print(db._getTimeframeStatement(a,b))

    print(db._getStationsStatement(('AAAA', 'BBBB', 'CCCC', 'DDDD')))