from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from point import Point
from rotation import Rotation
import ellipsoid
import scipy.constants
from scipy.integrate import solve_ivp
from scipy import interpolate
from glonassorbitdiffeq import *
import logging

class SatError(Exception):pass

SP3 = 1
BRDC = 2

class Satellite(object):
    """!Satellite class for contain and calc position
    """
    def __new__(self, prn='', nav={}):
        if prn[0] == 'G':
            return GPSSat(prn, nav)
        elif prn[0] == 'E':
            return GalileoSat(prn, nav)
        elif prn[0] == 'R':
            return GLONASSSat(prn, nav)

    def __init__(self, prn='', nav={}, coords=[]):
        """Satellite constructor
        @param prn (str): satellite PRN, default: ''
        @param nav (dict): navigation message, default: {}
        @partam coords (numoy array): list of coordinates, default: []
        """
        self.system = prn[0]
        self.prn = (prn)
        self.coords = []
        self.navigationDatas = []
        self.source = None
    @property
    def l1(self):
        """!get wavelength of L1 frequency
        @return (float): wavelength of L1 frquency
        """
        return scipy.constants.c/self.f1
    @property
    def l2(self):
        """!get wavelength of L2 frequency
        @return (float): wavelength of L2 frquency
        """
        return scipy.constants.c/self.f2
    @property
    def l5(self):
        """!get wavelength of L5 frequency
        @return (float): wavelength of L5 frquency
        """
        return scipy.constants.c/self.f5

    def getTimeFrameByElevAzimuthMask(self, elevation, azimuth, st):
        epochs = self.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
        start = epochs[0]
        end = epochs[-1]



        return np.array([start, end])

    def addNavMess(self, nav):
        """add new navigation message of an epoch

        @param nav (dictionary): navigation message

        """
        self.navigationDatas.append(nav)
        self.source = BRDC

    def addSP3coords(self, coords):
        """add new coordinates to satellite

        @param coords (numpy array): list of coordinates from SP3 file

        """
        self.coords = coords
        self.source = SP3

    def getElevAzimuth(self, st, epoch):
        """get elevetion and azimuth angle from point at epoch
        @param st (Point): refernce station
        @param epoch (Epoch): reference epoch
        @return (numpy array): elevation and azimuth angle in radian
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

        @param timeDiff (Epoch): difference between 2 epoch (Epoch), default: Epoch(np.array([0,0,0,0,15,0]))
        @return (list, Epoch): list of epochs in the valid time frame
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



    def getSatPosSP3(self, epoch):
        """!get position of the satellite at the given epoch
        @param epoch (Epoch): reference epoch
        @return (Point): position of the satellite at the given apoch
        
        """
        #print(np.shape(self.coords))
        #print(self.coords)

        return Point(coord=self.coords[np.where(self.coords[:,0] == epoch)[0], 1:4], system=ellipsoid.WGS84())

    def getSatPosNav(self, epoch):
        """!get position of the satellite at the given epoch
        @param epoch (Epoch): reference epoch
        @return (Point): position of the satellite at the given apoch
        
        """
        if self.system == 'G':#GPS satellite
            return self._getGPSSatPos(epoch)
        elif self.system == 'R':pass#GLONASS satellite
        elif self.system == 'E':pass#Galileo satellite

    def getSatPos(self, epoch):
        """!get position of the satellite at the given epoch
        @param epoch (Epoch): reference epoch
        @return (Point): position of the satellite at the given apoch
        
        """
        if self.source == BRDC:
            return self.getSatPosNav(epoch)
        elif self.source == SP3:
            return self.getSatPosSP3(epoch)





class GPSSat(Satellite):
    """!GPS Satellite class for contain and calculate position
    """
    f1 = 1575.42*10**6#Hz
    f2 = 1227.60*10**6#Hz
    f5 = 1176.45*10**6#Hz

    def __new__(self, prn='', nav={}):
        return object.__new__(self)

    def getValidEph(self, epoch):
        """!get valid navigation message for an epoch

        @param epoch (Epoch): reference epoch
        @return (list): valid nevigation message
        """
        #valid time frame from epoch
        min = epoch - Epoch(np.array([0, 0, 0, 1, 0, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 1, 0, 0]))


        for nav in self.navigationDatas:#check all navigation message epoch
            if min <= nav['epoch'] and nav['epoch'] <= max:#if navigation message is in the time frame

                return nav
                break#break loop when valid epoch is finded
        raise TimeError("Epoch out of time frame!")

    def getSatPosNav(self, epoch):
        """!get satellite position in case of GPS satellite

        @param epoch (Epoch): timestamp when we get the position of satellite
        @return (Point): position of satellite at given epoch
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
        coordsOrbPlane = Point(coord=np.array([rk*math.cos(uk), rk*math.sin(uk), 0]).T)

        #longitude of ascending node
        OMEGAk = ephemerids['OMEGA'] + (ephemerids['OMEGADOT'] - omegaE)*tk - omegaE*ephemerids['TOE']

        #Rotation about z axis with longitude of ascending node
        #and about x axis with inclination
        R = Rotation(x=ik, z=OMEGAk, order="zxy")

        p = R*coordsOrbPlane
        p.system = ellipsoid.WGS84()
        return p


    @property
    def T1(self):
        """!get L1 period time
        @return (float): L1 period time in seconds
        """
        return 1/self.f1
    @property
    def T2(self):
        """!get L2 period time
        @return (float): L2 period time in seconds
        """
        return 1/self.f2
    @property
    def T5(self):
        """!get L5 period time
        @return (float): L5 period time in seconds
        """
        return 1/self.f5

class GLONASSSat(Satellite):
    """!GLONASS Satellite class for contain and calculate position
    """
    def __new__(self, prn='', nav={}):
        return object.__new__(self)

    def __init__(self, prn='', nav={}):
        """!GLONASSSat initilaizer
        @param prn (str): PRN number
        @param nav (dict): navigation messages
        """
        super(GLONASSSat, self).__init__(prn, nav)
        self.diffEqSolved = np.empty((0,8))

    @property
    def f1(self):
        """!get L1 frequency of the satellite
        @return (float): L1 frequency in Hz
        """
        return (1602 + self.navigationDatas[0]['freqNum']*0.5625)*10**6

    @property
    def f2(self):
        """!get L2 frequency of the satellite
        @return (float): L2 frequency in Hz
        """
        return (1246 + self.navigationDatas[0]['freqNum']*0.4375)*10**6


    def getValidEph(self, epoch):
        """!get valid navigation message for epoch
        @param epoch (Epoch): timestamp what of valid nav message for (Epoch)
        @return (list): valid navigation message
        """
        #valid time frame from epoch
        min = epoch - Epoch(np.array([0, 0, 0, 0, 15, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 0, 15, 0]))


        for nav in self.navigationDatas:#check all navigation message epoch
            if min <= nav['epoch'] and nav['epoch'] <= max:#if navigation message is in the time frame

                return nav
                break#break loop when valid epoch is finded
        raise TimeError("Epoch out of time frame!")


    def getSatPosNav(self, epoch):
        """!get satellite position in case of GLONASS satellite
        @param epoch (Epoch): timestamp when of the position of satellite
        @return (Point): position of satellite at given epoch
        """


        ephemerids = self.getValidEph(epoch)




        solvedEqIndex = np.where(self.diffEqSolved[:,0] == ephemerids['epoch'])

        if np.shape(solvedEqIndex) == (1,0):



            Y0 = [
            ephemerids['x0'],
            ephemerids['y0'],
            ephemerids['z0'],
            ephemerids['dxdt'],
            ephemerids['dydt'],
            ephemerids['dzdt']
            ]

            #print(np.append(epoch, Y0))

            #print(Y0)
            #print(params)



            soleq1 = scipy.integrate.solve_ivp(fun=lambda t, w: diffeq(t, w, ephemerids['dxdt2'], ephemerids['dydt2'], ephemerids['dzdt2']), t_span=[0, -901], y0=Y0, method='RK45', t_eval=list(range(-1, -902, -1)), max_step=10)
            soleq2 = scipy.integrate.solve_ivp(fun=lambda t, w: diffeq(t, w, ephemerids['dxdt2'], ephemerids['dydt2'], ephemerids['dzdt2']), t_span=[0, 901], y0=Y0, method='RK45', t_eval=list(range(0, 902)), max_step=10)
            #print(2)

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

            #print(np.shape(sol))
            #print(sol[880:885,:])
            self.diffEqSolved = np.append(self.diffEqSolved, sol, axis=0)

        dt = ephemerids['tauN'] - ephemerids['gammaN']*(epoch.TOW - ephemerids['epoch'].TOW)

        tk = epoch.TOW - ephemerids['epoch'].TOW + dt

        #print(tk)
        while tk > 3600:
            tk = tk - 604800
        while tk < -3600:

            tk = tk + 604800

        solvedEqIndex = np.where(self.diffEqSolved[:,0] == ephemerids['epoch'])

        fx = interpolate.interp1d(self.diffEqSolved[solvedEqIndex][:,1], self.diffEqSolved[solvedEqIndex][:,2])
        fy = interpolate.interp1d(self.diffEqSolved[solvedEqIndex][:,1], self.diffEqSolved[solvedEqIndex][:,3])
        fz = interpolate.interp1d(self.diffEqSolved[solvedEqIndex][:,1], self.diffEqSolved[solvedEqIndex][:,4])
        return Point(coord=np.array([fx(tk), fy(tk), fz(tk)]), system=ellipsoid.WGS84())




class GalileoSat(Satellite):
    """!GLONASS Satellite class for contain and calculate position
    """
    f1 = 1575.42*10**6#Hz
    f5 = 1191.795*10**6#Hz
    f5a = 1176.45*10**6#Hz
    f5b = 1207.14*10**6#Hz
    f6 = 1278.750*10**6#Hz

    def __new__(self, prn='', nav={}):
        return object.__new__(self)

    def getValidEph(self, epoch):
        """!get valid navigation message for an epoch

        @param epoch (Epoch): reference epoch
        @return (list): valid nevigation message
        """
        #valid time frame from epoch
        min = epoch - Epoch(np.array([0, 0, 0, 0, 5, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 0, 5, 0]))


        for nav in self.navigationDatas:#check all navigation message epoch
            if min <= nav['epoch'] and nav['epoch'] <= max:#if navigation message is in the time frame

                return nav
                break#break loop when valid epoch is finded
        raise TimeError("Epoch out of time frame!")

    def getSatPosNav(self, epoch):
        """!get satellite position in case of GPS satellite

        @param epoch (Epoch): timestamp when we get the position of satellite
        @return (Point): position of satellite at given epoch
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
        R = Rotation(x=ik, z=OMEGAk, order="zxy")
        p = R*coordsOrbPlane
        p.system = ellipsoid.WGS84()
        return p


    @property
    def T1(self):
        """!get L1 period time
        @return (float): L1 period time in seconds
        """
        return 1/self.f1
    @property
    def T5(self):
        """!get L5 period time
        @return (float): L5 period time in seconds
        """
        return 1/self.f5
    @property
    def T5a(self):
        """!get L5a period time
        @return (float): L5a period time in seconds
        """
        return 1/self.f5a
    @property
    def T5b(self):
        """!get L5b period time
        @return (float): L5b period time in seconds
        """
        return 1/self.f5b
    @property
    def T6(self):
        """!get L6 period time
        @return (float): L6 period time in seconds
        """
        return 1/self.f6
