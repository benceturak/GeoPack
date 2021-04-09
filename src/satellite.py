from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from point import Point
from rotation import Rotation
import logging

class Satellite(object):
    """
        Satellite class for contain and calc position

            :param prn: satellite PRN
            :param nav: navigation message (dictionary)
    """
    def __init__(self, prn='', nav={}):
        """Satellite constructor

        """
        self.system = prn[0]
        self.prn = (prn)
        self.navigationDatas = []

    def addNavMess(self, nav):
        """add new navigation message of epoch

                :param nav: navigation message (dictionary)

        """
        self.navigationDatas.append(nav)

    def getEpochsInValidTimeFrame(self, timeDiff=Epoch(np.array([0,0,0,0,15,0]))):
        """method to get epochs in the given messages valid time frame
            :param timeDiff: difference between 2 epoch (Epoch), default 15 minutes
            :return: list of epochs in the valid time frame
        """
        epochs = np.empty((1,0))

        for nav in self.navigationDatas:
            begin = nav['epoch'] - Epoch(np.array([0,0,0,1,0,0]))

            end = nav['epoch'] + Epoch(np.array([0,0,0,1,0,0]))
            e = begin
            while True:
                epochs = np.append(epochs,  [[e]], axis=1)
                e += timeDiff
                if e > end:
                    epochs = np.append(epochs,  [[end]], axis=1)
                    break
            return epochs


    def getValidEph(self, epoch):
        """get valid navigation message for epoch

                :param epoch: timestamp what we get valid nav message for (Epoch)
        """
        #valid time frame from epoch
        min = epoch - Epoch(np.array([0, 0, 0, 1, 0, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 1, 0, 0]))


        for nav in self.navigationDatas:#check all navigation message epoch
            if min <= nav['epoch'] and nav['epoch'] <= max:#if navigation message is in the time frame

                return nav
                break#break loop when valid epoch is finded
        raise TimeError("Epoch out of time frame!")


    def getSatPos(self, epoch):
        """get satellite position at an epoch

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        if self.system == 'G':#GPS satellite
            return self._getGPSSatPos(epoch)
        elif self.system == 'R':pass#GLONASS satellite
        elif self.system == 'E':pass#Galileo satellite

    def _getGPSSatPos(self, epoch):
        """get satellite position in case of GPS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        #get valid navigation data to calculate the satellite position
        ephemerids = self.getValidEph(epoch)

        GM = 3.986005*10**14
        omegaE = 7.2921151467*10**(-5)

        ## TODO: handle the epochs on the GPS weeks borders
        tk = epoch.getTOW - ephemerids['TOE']

        n0 = math.sqrt(GM/ephemerids['a']**3)#mean motion
        n = n0 + ephemerids['deltan']#mean motion difference
        Mk = ephemerids['M0'] + n*tk#mean anomaly

        Ek = Mk
        d = 1#difference
        #eccentricity anomaly (iterative)
        while abs(d) > 10**(-12):#iteration is ended when the difference between two following step less then 10e-12
            E_l = Ek
            Ek = Mk + ephemerids['e']*math.sin(Ek)
            d = abs(Ek - E_l)

        #true anomaly
        nu = 2*math.atan(math.sqrt(1 + ephemerids['e'])/math.sqrt(1 - ephemerids['e'])*math.tan(Ek/2))

        phik = nu + ephemerids['omega']

        #correction of argument of latitude
        duk = ephemerids['Cuc']*math.cos(2*phik) + ephemerids['Cus']*math.sin(2*phik)
        #correction of radial distance
        drk = ephemerids['Crc']*math.cos(2*phik) + ephemerids['Crs']*math.sin(2*phik)
        #correction of inclination
        dik = ephemerids['Cic']*math.cos(2*phik) + ephemerids['Cis']*math.sin(2*phik)

        #argument of latitude
        uk = phik + duk
        #radial distance
        rk = ephemerids['a']*(1 - ephemerids['e']*math.cos(Ek)) + drk
        #inclination
        ik = ephemerids['i0'] + ephemerids['idot']*tk + dik

        #coordinates in the satellite's orbit plane
        coordsOrbPlane = Point(coord=np.array([rk*math.cos(uk), rk*math.sin(uk), 0]).T)

        #longitude of ascending node
        OMEGAk = ephemerids['OMEGA'] + (ephemerids['OMEGADOT'] - omegaE)*tk - omegaE*ephemerids['TOE']

        #Rotation about z axis with longitude of ascending node
        #and about x axis with inclination
        R = Rotation(x=ik, z=OMEGAk, orther="zxy")

        return R*coordsOrbPlane
