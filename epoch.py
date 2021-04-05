import numpy as np
import datetime
import math

class Epoch(object):

    def __init__(self, dt):


        self.dt = dt

    @property
    def getUTC(self):
        return self.dt


    @property
    def getGPSweek(self):

        return int((math.floor(math.floor(self.getMJD()) - Epoch(np.array([1980,1,6,0,0,0])).getMJD()))/7)


    @property
    def getTOW(self):

        return (self.getMJD() - int(self.getMJD()))*24*3600

    @property
    def getDOW(self):
        return (math.floor(math.floor(self.getMJD()) - Epoch(np.array([1980,1,6,0,0,0])).getMJD()))%7

    @property
    def getGPStime(self):

        return np.array([self.getGPSweek, self.getTOW, self.getDOW])


    def getMJD(self):
        #leapsec???????
        return datetime.date.toordinal(datetime.date(int(self.dt[0]),int(self.dt[1]),int(self.dt[2]))) + (self.dt[3] + (self.dt[4] + self.dt[5]/60)/60)/(24) - 678576





    def _normalize(self):
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        #seconds
        while self.dt[5] > 60:
            self.dt[5] -= 60
            self.dt[4] += 1
        while self.dt[5] < 0:
            self.dt[5] += 60
            self.dt[4] -= 1
        #minutes
        while self.dt[4] > 60:
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

        daysOfMonth = months[m-1]

        if self.dt[0] % 4 == 0 and m == 1:
            daysOfMonth += 1

        while self.dt[2] > daysOfMonth:
            self.dt[2] -= daysOfMonth
            self.dt[1] += 1
        while self.dt[2] < 0:
            self.dt[2] += daysOfMonth
            self.dt[1] -= 1

        #months

        while self.dt[1] > 12:
            self.dt[1] -= 12
            self.dt[0] += 1
        while self.dt[1] < 0:
            self.dt[1] += 12
            self.dt[0] -= 1

        return self


    def __eq__(self, other):
        return (self.dt == other.dt).all()

    def __neq__(self, other):
        return not (self.dt == other.dt).all()

    def __gt__(self, other):
        for i in np.append([self.dt == other.dt], [self.dt > other.dt], axis=0).T:
            if not i[0] and i[1]:
                return True
                break
        return False

    def __lt__(self, other):
        for i in np.append([self.dt == other.dt], [self.dt < other.dt], axis=0).T:
            if not i[0] and i[1]:
                return True
                break
        return False

    def __ge__(self, other):
        return self > other or self == other
    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
        return Epoch(self.dt + other.dt)._normalize()

    def __sub__(self, other):
        return Epoch(self.dt - other.dt)._normalize()

    def __repr__(self):
        return '[{0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:.5f}]'.format(int(self.dt[0]), int(self.dt[1]), int(self.dt[2]), int(self.dt[3]), int(self.dt[4]), self.dt[5])


if __name__ == "__main__":

    a = Epoch(np.array([2021,4,18,15,0,0]))
    b = Epoch(np.array([0,8,27,7,0,0]))
    c = Epoch(np.array([2019,4,2,8,0,0]))

    #print(a  b)
    print(a>=c)
    print(c<a)

    print(a.getGPSweek)
    print(a.getTOW)
    print(a.getDOW)
