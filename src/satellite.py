from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from point import Point
from rotation import Rotation
import ellipsoid
import scipy.constants
import scipy.integrate
import logging

class SatError(Exception):pass

class Satellite(object):
    """
        Satellite class for contain and calc position

            :param prn: satellite PRN
            :param nav: navigation message (dictionary)
    """
    def __new__(self, prn='', nav={}):
        if prn[0] == 'G':
            return GPSSat(prn, nav)
        elif prn[0] == 'E':
            return GalileoSat(prn, nav)
        elif prn[0] == 'R':
            return GLONASSSat(prn, nav)

    def __init__(self, prn='', nav={}):
        """Satellite constructor

        """
        self.system = prn[0]
        self.prn = (prn)
        self.navigationDatas = []

    def getTimeFrameByElevAzimuthMask(self, elevation, azimuth, st):
        epochs = self.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
        start = epochs[0]
        end = epochs[-1]



        return np.array([start, end])









    def addNavMess(self, nav):
        """add new navigation message of epoch

            :param nav: navigation message (dictionary)

        """
        self.navigationDatas.append(nav)

    def getElevAzimuth(self, st, epoch):
        """get elevetion and azimuth angle from point at epoch
            :param st: (Point)
            :param epoch:

            :return: elevation and azimuth angle in numpy vector (ndarray)
        """
        if not isinstance(st, Point):
            raise TypeError("st must be Point type!")
        if not isinstance(epoch, Epoch):
            raise TypeError("epoch must be Epoch type!")


        #st = Point(coord=np.array([0,6500000,0]), system=WGS84())

        R = Rotation()

        R.setRot(np.array([[-math.sin(st.plh[0,0])*math.cos(st.plh[1,0]), -math.sin(st.plh[0,0])*math.sin(st.plh[1,0]), math.cos(st.plh[0,0])], [-math.sin(st.plh[1,0]), math.cos(st.plh[1,0]), 0], [math.cos(st.plh[0,0])*math.cos(st.plh[1,0]), math.cos(st.plh[0,0])*math.sin(st.plh[1,0]), math.sin(st.plh[0,0])]]))

        topo = R * (self.getSatPos(epoch) - st)
        return np.array([math.atan(topo.xyz[2,0]/math.sqrt(topo.xyz[0,0]**2 + topo.xyz[1,0]**2)), math.atan2(topo.xyz[1,0],topo.xyz[0,0])])


    def getEpochsInValidTimeFrame(self, timeDiff=Epoch(np.array([0,0,0,0,15,0]))):
        """method to get epochs in the given messages valid time frame

            :param timeDiff: difference between 2 epoch (Epoch), default 15 minutes
            :return: list of epochs in the valid time frame (np.ndarray(Epoch))
        """

        #initalize vars
        epochs = np.empty((0,))
        ends = np.empty((0,))


        #check navigation datas message by message
        for nav in self.navigationDatas:
            #begin of frame
            begin = nav['epoch'] - Epoch(np.array([0,0,0,1,0,0]))
            #end of frame
            end = nav['epoch'] + Epoch(np.array([0,0,0,1,0,0]))

            #store all end of frame for check the duplicate epochs on borders
            ends = np.append(ends, end)

            ep = begin
            #check borders
            for e in ends:
                #if present frame begin with the lasts' epoch skip the first epoch
                if e == begin:
                    ep += timeDiff
            #store every epoch with timeDiff differences while reaches the end
            while ep < end:

                epochs = np.append(epochs,  [ep])
                ep += timeDiff
            #if last ep greater then end
            if ep > end:
                #append end of frame to the list
                epochs = np.append(epochs,  [end])
        return epochs





    def getSatPos(self, epoch):
        """get satellite position at an epoch

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        if self.system == 'G':#GPS satellite
            return self._getGPSSatPos(epoch)
        elif self.system == 'R':pass#GLONASS satellite
        elif self.system == 'E':pass#Galileo satellite



class GPSSat(Satellite):
    f1 = 1575.42*10**6#Hz
    f2 = 1227.60*10**6#Hz
    f5 = 1176.45*10**6#Hz

    def __new__(self, prn='', nav={}):
        return object.__new__(self)

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
        """get satellite position in case of GPS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        #get valid navigation data to calculate the satellite position
        ephemerids = self.getValidEph(epoch)

        GM = 3.986005*10**14
        omegaE = 7.2921151467*10**(-5)

        ## TODO: handle the epochs on the GPS weeks borders
        tk = epoch.TOW - ephemerids['TOE']

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
        coordsOrbPlane = Point(coord=np.array([rk*math.cos(uk), rk*math.sin(uk), 0]).T, system=ellipsoid.WGS84())

        #longitude of ascending node
        OMEGAk = ephemerids['OMEGA'] + (ephemerids['OMEGADOT'] - omegaE)*tk - omegaE*ephemerids['TOE']

        #Rotation about z axis with longitude of ascending node
        #and about x axis with inclination
        R = Rotation(x=ik, z=OMEGAk, orther="zxy")

        return R*coordsOrbPlane
    @property
    def l1(self):
        return scipy.constants.c/self.f1
    @property
    def l2(self):
        return scipy.constants.c/self.f2
    @property
    def l5(self):
        return scipy.constants.c/self.f5

    @property
    def T1(self):
        return 1/self.f1
    @property
    def T2(self):
        return 1/self.f2
    @property
    def T5(self):
        return 1/self.f5

class GLONASSSat(Satellite):
    def __new__(self, prn='', nav={}):
        return object.__new__(self)

    def getValidEph(self, epoch):
        """get valid navigation message for epoch

                :param epoch: timestamp what we get valid nav message for (Epoch)
        """
        #valid time frame from epoch
        min = epoch - Epoch(np.array([0, 0, 0, 0, 15, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 0, 15, 0]))


        for nav in self.navigationDatas:#check all navigation message epoch
            if min <= nav['epoch'] and nav['epoch'] <= max:#if navigation message is in the time frame

                return nav
                break#break loop when valid epoch is finded
        raise TimeError("Epoch out of time frame!")

    def getSatPos(self, epoch):
        """get satellite position in case of GLONASS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        aE = 6378136#m
        omegaE = 0.7292115*10^-4#rad/s
        mu = 39860044*10^14#m^3/s^2
        C20 = -1.08263*10^-3


        r = lambda x,y,z: math.sqrt(x^2 + y^2 + z^2)

        dxdt = lambda vx: vx
        dydt = lambda vy: vy
        dzdt = lambda vz: vz

        dxdt2 = lambda x, z, ax, vy: -mu/r(x, y, z)^3*x + 3/2*C20*mu*aE^2/r(x, y, z)^5*x*(1-5*z^2/r(x, y, z)^2) + ax + omegaE^2*x + 2*omegaE*vy
        dydt2 = lambda y, z, ay, vx: -mu/r(x, y, z)^3*y + 3/2*C20*mu*aE^2/r(x, y, z)^5*y*(1-5*z^2/r(x, y, z)^2) + ay + omegaE^2*y + 2*omegaE*vx
        dzdt2 = lambda z: -mu/r(x, y, z)^3*z + 3/2*C20*mu*aE^2/r(x, y, z)^5*z*(1-5*z^2/r(x, y, z)^2 )





































class GalileoSat(Satellite):pass
