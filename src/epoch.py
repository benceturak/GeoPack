import numpy as np
import datetime
import math
import wget
import urllib
import os
import logging

GPS = 1
UTC = 2

class TimeError(Exception):pass

class Epoch(object):
    """
        Epoch class to contain datetime and perform operations

            :param dt: datetime in vector [year, month, day, hour, minute, second](NumPy array)
            :param system: time system GPS, UTC (int), default GPS
    """

    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, dt, system=GPS, downloadLeapSec=False):
        """Epoch constructor

        """

        if system == GPS:
            self.dt = dt
        elif system == UTC:
            self.dt = dt
            ls = LeapSecs(download=downloadLeapSec).getLeapSecsAt(self)
            #print(self + ls)
            self.dt = (self + ls).dt

    @property
    def getDateTime(self, system=GPS):
        """get DateTime time

        """
        return self.dt


    @property
    def GPSweek(self):
        """get GPS week
            :return: DOW (int)
        """
        return int((math.floor(math.floor(self.MJD) - Epoch(np.array([1980,1,6,0,0,0])).MJD))/7)


    @property
    def TOW(self):
        """get seconds on the GPS week
            :return: TOW(float)
        """
        return self.DOW*86400 + self.dt[3]*3600 + self.dt[4]*60 + self.dt[5]

    @property
    def DOW(self):
        """get day of GPS week
            :return: DOW (int)
        """
        return int((math.floor(math.floor(self.MJD) - Epoch(np.array([1980,1,6,0,0,0])).MJD))%7)

    @property
    def DOY(self):
        """get day of year
            :return: DOY (int)
        """
        DOY = 0
        for i in range(0,self.dt[1]-1):
            DOY = DOY + self.months[i]

        if self.dt[0] % 4 == 0 and m == 1:#leap year, february
            DOY = DOY + 1
        DOY = DOY + self.dt[2]

        return DOY




    @property
    def UTC(self):
        ls = LeapSecs().getLeapSecsAt(self)
        return (self - ls).dt
    @property
    def GPS(self):
        return self.dt

    @property
    def MJD(self):
        """get Modified Julian Date
            :return: MJD (float)
        """
        #leapsec???????
        return datetime.date.toordinal(datetime.date(int(self.dt[0]),int(self.dt[1]),int(self.dt[2]))) + (self.dt[3] + (self.dt[4] + self.dt[5]/60)/60)/(24) - 678576





    def _normalize(self):
        """normalize date when a value out of range

        """

        #seconds
        while self.dt[5] > 59:
            self.dt[5] -= 60
            self.dt[4] += 1
        while self.dt[5] < 0:
            self.dt[5] += 60
            self.dt[4] -= 1
        #minutes
        while self.dt[4] > 59:
            self.dt[4] -= 60
            self.dt[3] += 1
        while self.dt[4] < 0:
            self.dt[4] += 60
            self.dt[3] -= 1

        #hour
        while self.dt[3] > 23:
            self.dt[3] -= 24
            self.dt[2] += 1
        while self.dt[3] < 0:
            self.dt[3] += 24
            self.dt[2] -= 1

        #day
        m = int(self.dt[1])
        while m > 12:
            m -= 12
        while m < 0:
            m += 12

        daysOfMonth = self.months[m-1]

        if self.dt[0] % 4 == 0 and m == 1:#leap year, february
            daysOfMonth += 1

        while self.dt[2] > daysOfMonth:
            self.dt[2] -= daysOfMonth
            self.dt[1] += 1
        while self.dt[2] < 1:
            self.dt[2] += daysOfMonth
            self.dt[1] -= 1

        #months
        while self.dt[1] > 12:
            self.dt[1] -= 12
            self.dt[0] += 1
        while self.dt[1] < 1:
            self.dt[1] += 12
            self.dt[0] -= 1



    def __eq__(self, other):
        return (self.dt == other.dt).all()

    def __neq__(self, other):
        return not self == other

    def __gt__(self, other):
        for i in np.array([self.dt == other.dt, self.dt < other.dt, self.dt > other.dt]).T:
            if i[1]:
                return False
                break
            if not i[0] and i[2]:
                return True
                break
        return False

    def __lt__(self, other):
        for i in np.array([self.dt == other.dt, self.dt < other.dt, self.dt > other.dt]).T:
            if i[2]:
                return False
                break
            if not i[0] and i[1]:
                return True
                break
        return False

    def __ge__(self, other):
        return self > other or self == other
    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
        re = Epoch(self.dt + other.dt)
        re._normalize()
        return re

    def __sub__(self, other):
        re = Epoch(self.dt - other.dt)
        re._normalize()
        return re

    def __repr__(self):

        return '[{0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:.5f}]'.format(int(self.dt[0]), int(self.dt[1]), int(self.dt[2]), int(self.dt[3]), int(self.dt[4]), self.dt[5])

    def __str__(self):

        return '{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:05.2f}'.format(int(self.dt[0]), int(self.dt[1]), int(self.dt[2]), int(self.dt[3]), int(self.dt[4]), self.dt[5])
class LeapSecs(object):
    """
        LeapSecs class to handle leap seconds
            :param fileName: (string), default Leap_second.dat
            :param url: url of leapsec file (string), default https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat (IERS bulletin C)
            :param download: download the leapsec file? (boolean), default False
    """

    def __init__(self, fileName = 'Leap_Second.dat', url='https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat', download=False):
        """LeapSecs construcor

        """
        self.fileName = fileName
        self.leapSecs = np.empty((0,3))

        try:
            if download:#download leap seconds file if necessary
                if os.path.exists(fileName):
                    os.remove(fileName)
                wget.download(url, fileName)
                print()
            self.fid = open(self.fileName, 'r')

            self._read()
        except urllib.error.HTTPError:
            logging.error("Leapsec file connet be downloaded!")
        finally:
            self.fid.close()

    def _read(self):
        """read leapsec file

        """

        #read leeapsec file row by row
        while True:
            line = self.fid.readline()
            if line[0:1] == "#":#header rows
                pass#print(line)
            elif line[0:1] == " ":#content
                self.leapSecs = np.append(self.leapSecs, [[float(line[0:13].strip()), Epoch(np.array([int(line[19:24].strip()), int(line[16:19].strip()), int(line[13-16].strip()),0,0,0])), int(line[24:33].strip())]], axis=0)
            else:
                break

    def getLeapSecsAt(self, epoch, fr=GPS):
        for i in self.leapSecs:
            if i[1] <= epoch:
                ls = i[2]
            else:
                break

        return Epoch(np.array([0,0,0,0,0,ls-19]))


if __name__ == "__main__":

    #print(ls.leapSecs)
    a = Epoch(np.array([2021,4,18,23,0,0]), system=GPS)
    b = Epoch(np.array([0,8,27,7,0,60]))
    c = Epoch(np.array([1998,4,18,15,0,0]), system=UTC, downloadLeapSec=True)
    #print(c.dt)
    ls = LeapSecs()
    #print(ls.getLeapSecsAt(c))

    print(a.dt)
    print(a.UTC)
    #print(a.SU)

    #print(a + b)
    #print(a+b)
    #print(c<a)

    #print(a.getGPSweek)
    #print(a.getTOW)
    #print(a.getDOW)
