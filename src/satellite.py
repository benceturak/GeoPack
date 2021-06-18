from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from point import Point
from rotation import Rotation
import ellipsoid
import scipy.constants
from scipy.integrate import solve_ivp
from glonassorbitdiffeq import *
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
    @property
    def l1(self):
        return scipy.constants.c/self.f1
    @property
    def l2(self):
        return scipy.constants.c/self.f2
    @property
    def l5(self):
        return scipy.constants.c/self.f5

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

        tk = epoch.TOW - ephemerids['TOE']
        while tk > 3600:
            tk = tk - 604800
        while tk < -3600:
            tk = tk + 604800
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

    def __init__(self, prn='', nav={}):
        super(GLONASSSat, self).__init__(prn, nav)
        self.diffEqSolved = np.empty((0,8))

    @property
    def f1(self):
        return (1602 + self.navigationDatas[0]['freqNum']*0.5625)*10**6

    @property
    def f2(self):
        return (1246 + self.navigationDatas[0]['freqNum']*0.4375)*10**6


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


        ephemerids = self.getValidEph(epoch)




        solvedEqIndex = np.where(self.diffEqSolved[:,0] == ephemerids['epoch'])
        if np.shape(solvedEqIndex) == (1,0):

            print('1')

            Y0 = [
            ephemerids['x0'],
            ephemerids['y0'],
            ephemerids['z0'],
            ephemerids['dxdt'],
            ephemerids['dydt'],
            ephemerids['dzdt']
            ]
            #print(t_GLO)
            params = [
            ephemerids['dxdt2'],
            ephemerids['dydt2'],
            ephemerids['dzdt2']
            ]



            soleq1 = scipy.integrate.solve_ivp(diffeq, [0, -901], Y0, method='RK45', t_eval=list(range(-1, -902, -1)), args=params, max_step=10)
            soleq2 = scipy.integrate.solve_ivp(diffeq, [0, 901], Y0, method='RK45', t_eval=list(range(0, 902)), args=params, max_step=10)


            sol1 = np.full((1,901), ephemerids['epoch'])
            sol1 = np.append(sol1, [soleq1.t], axis=0)
            sol1 = np.append(sol1, [soleq1.y[0,:]], axis=0)
            sol1 = np.append(sol1, [soleq1.y[1,:]], axis=0)
            sol1 = np.append(sol1, [soleq1.y[2,:]], axis=0)
            sol1 = np.append(sol1, [soleq1.y[3,:]], axis=0)
            sol1 = np.append(sol1, [soleq1.y[4,:]], axis=0)
            sol1 = np.append(sol1, [soleq1.y[5,:]], axis=0)

            sol1 = sol1.T

            sol1 = sol1[np.argsort(sol1[:,1]),:]

            sol2 = np.full((1,902), ephemerids['epoch'])
            sol2 = np.append(sol2, [soleq2.t], axis=0)
            sol2 = np.append(sol2, [soleq2.y[0,:]], axis=0)
            sol2 = np.append(sol2, [soleq2.y[1,:]], axis=0)
            sol2 = np.append(sol2, [soleq2.y[2,:]], axis=0)
            sol2 = np.append(sol2, [soleq2.y[3,:]], axis=0)
            sol2 = np.append(sol2, [soleq2.y[4,:]], axis=0)
            sol2 = np.append(sol2, [soleq2.y[5,:]], axis=0)

            sol2 = sol2.T

            sol = np.append(sol1, sol2, axis=0)



            self.diffEqSolved = np.append(self.diffEqSolved, sol, axis=0)

        solvedEqIndex = np.where(self.diffEqSolved[:,0] == ephemerids['epoch'])

        dt = ephemerids['tauN'] - ephemerids['gammaN']*(epoch.TOW - ephemerids['epoch'].TOW)

        tk = epoch.TOW - ephemerids['epoch'].TOW + dt

        #print(tk)
        while tk > 3600:
            tk = tk - 604800
        while tk < -3600:

            tk = tk + 604800

        border_cond = np.append([self.diffEqSolved[:,0] == ephemerids['epoch']], [self.diffEqSolved[:,1] == math.floor(tk)], axis=0)
        border_cond = np.append(border_cond, [self.diffEqSolved[:,1] == math.ceil(tk)], axis=0)

        #print(tk)
        #tk_border =
        border_low = self.diffEqSolved[np.where(border_cond[(0,1),:].all(axis=0))]
        border_heigh = self.diffEqSolved[np.where(border_cond[(0,2),:].all(axis=0))]

        #print(border_low)
        #print(border_heigh)
        #print(epoch)
        #print('------------------------')


        if border_low[0,1] == border_heigh[0,1]:
            px = border_low[0,2]
            py = border_low[0,3]
            pz = border_low[0,4]
        else:
            px = border_low[0,2] + (tk - border_low[0,1])/(tk - border_heigh[0,1])*(border_heigh[0,2] - border_low[0,2])
            py = border_low[0,3] + (tk - border_low[0,1])/(tk - border_heigh[0,1])*(border_heigh[0,3] - border_low[0,3])
            pz = border_low[0,4] + (tk - border_low[0,1])/(tk - border_heigh[0,1])*(border_heigh[0,4] - border_low[0,4])

        return Point(coord=np.array([px, py, pz]))
        #tk - tk_border[1]
        #if tt < 0:
        #    epochIndex = np.where(self.diffEqSolved[solvedEqIndex[0][0],1].t == tk)
        #    return Point(coord=np.array([self.diffEqSolved[solvedEqIndex[0][0],1].y[0,epochIndex[0][0]], self.diffEqSolved[solvedEqIndex[0][0],1].y[1,epochIndex[0][0]], self.diffEqSolved[solvedEqIndex[0][0],1].y[2,epochIndex[0][0]]]))
        #elif tt >= 0:
        #    epochIndex = np.where(self.diffEqSolved[solvedEqIndex[0][0],2].t == tk)
        #    return Point(coord=np.array([self.diffEqSolved[solvedEqIndex[0][0],2].y[0,epochIndex[0][0]], self.diffEqSolved[solvedEqIndex[0][0],2].y[1,epochIndex[0][0]], self.diffEqSolved[solvedEqIndex[0][0],2].y[2,epochIndex[0][0]]]))





class GalileoSat(Satellite):pass
