from epoch import Epoch
import numpy as np
import math

class Satellite(object):

    def __init__(self, prn='', nav={}):
        self.system = prn[0]
        self.prn = (prn)
        self.navigationDatas = []

    def addNavMess(self, nav):
        self.navigationDatas.append(nav)

    def getValidEph(self, epoch):

        min = epoch - Epoch(np.array([0, 0, 0, 1, 0, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 1, 0, 0]))

        for nav in self.navigationDatas:

            if min <= nav['epoch'] and nav['epoch'] <= max:
                return nav
                break


    def getSatPos(self, epoch):
        if self.system == 'G':
            return self._getGPSSatPos(epoch)
        elif self.system == 'R':pass
        elif self.system == 'E':pass

    def _getGPSSatPos(self, epoch):

        ephemerids = self.getValidEph(epoch)

        t_temp = ephemerids['TOE']

        DOW = 0

        while t_temp >= 86400:
            t_temp -= 86400
            DOW += 1


        t = DOW*86400 + epoch.getUTC[3]*3600 + epoch.getUTC[4]*60 + epoch.getUTC[5]

        GM = 3.986005*10**14
        omegaE = 7.2921151467*10**(-5)

        tk = t - ephemerids['TOE']

        n0 = math.sqrt(GM/ephemerids['a']**3)
        n = n0 + ephemerids['deltan']
        Mk = ephemerids['M0'] + n*tk

        Ek = Mk

        d = 1
        while d > 10**(-12):
            E_l = Ek
            Ek = Mk + ephemerids['e']*math.sin(Ek)
            d = abs(Ek - E_l)

        nu = 2*math.atan(math.sqrt(1 + ephemerids['e'])/math.sqrt(1 - ephemerids['e'])*math.tan(Ek/2))

        phik = nu + ephemerids['omega']

        duk = ephemerids['Cuc']*math.cos(2*phik) + ephemerids['Cus']*math.sin(2*phik)
        drk = ephemerids['Crc']*math.cos(2*phik) + ephemerids['Crs']*math.sin(2*phik)
        dik = ephemerids['Cic']*math.cos(2*phik) + ephemerids['Cis']*math.sin(2*phik)

        uk = phik + duk
        rk = ephemerids['a']*(1 - ephemerids['e']*math.cos(Ek))+ drk
        ik = ephemerids['i0'] + ephemerids['idot']*tk + dik
        xk = rk*math.cos(uk)
        yk = rk*math.sin(uk)
        zk = 0

        coordsOrbPlane = np.array([[xk], [yk], [zk]])

        OMEGAk = ephemerids['OMEGA'] + (ephemerids['OMEGADOT'] - omegaE)*tk - omegaE*ephemerids['TOE']
        ROMEGA = np.array([[math.cos(OMEGAk), -math.sin(OMEGAk), 0], [math.sin(OMEGAk), math.cos(OMEGAk), 0], [0, 0, 1]])
        Ri = np.array([[1, 0, 0], [0, math.cos(ik), -math.sin(ik)], [0, math.sin(ik), math.cos(ik)]])


        coords = np.dot(np.dot(ROMEGA, Ri), coordsOrbPlane)

        return coords
