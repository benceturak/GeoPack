import numpy as np

class ReadDB(object):


    def __init__(self, db):
        self._database = db

    def getNw(self):
        pass

    def getZWD(self, stations=None, from=None, to=None):

        stations_statement = ''


        sql = 'SELECT STATION, DATE, TIME, ZWD WHERE CONSTELLATION=0'




if __name__ == "__main__":
    pass
