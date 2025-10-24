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

    def __init__(self, prn='', nav={}, coords=[]):
        """Satellite constructor

        """
        self.system = prn[0]
        self.prn = (prn)
        self.coords = []
        self.navigationDatas = []
        self.source = None
        self.GAGP = np.array([0,0,0,0])
    @property
    def l1(self):
        return scipy.constants.c/self.f1
    @property
    def l2(self):
        return scipy.constants.c/self.f2
    

    

    def getTimeFrameByElevAzimuthMask(self, elevation, azimuth, st):
        epochs = self.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
        start = epochs[0]
        end = epochs[-1]



        return np.array([start, end])

    def setGAGP(self, GAGP):
        self.GAGP = GAGP
    def addNavMess(self, nav):
        """add new navigation message of epoch

            :param nav: navigation message (dictionary)

        """
        self.navigationDatas.append(nav)
        self.source = BRDC

    def addSP3coords(self, coords):
        """add new coordinates to satellite

            :param coords: navigation message (dictionary)

        """
        self.coords = coords
        self.coords = np.append(self.coords, (self.coords[:,0:1]*604800 + self.coords[:,1:2]), axis=1)
        self.source = SP3

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
        pos, clk = self.getSatPos(epoch)
        topo = R * (pos - st)
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



    

    def getSatPosNav(self, epoch):
        """get satellite position at an epoch

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        if self.system == 'G':#GPS satellite
            return self._getGPSSatPos(epoch)
        elif self.system == 'R':pass#GLONASS satellite
        elif self.system == 'E':pass#Galileo satellite

    #def getSatClockErrorNav(self, epoch):
    #    """get satellite clock error at an epoch

    #            :param epoch: timestamp when we get the position of satellite (Epoch)
    #            :returns: clock error of satellite at given epoch (Point)
    #    """
    #    if self.system == 'G':#GPS satellite
    #        return self._getGPSSatClockError(epoch)
    #    elif self.system == 'R':pass#GLONASS satellite
    #    elif self.system == 'E':#Galileo satellite
    #        return self._getGalileoSatClockError(epoch)


    def getSatClockError(self, epoch):
        if self.source == BRDC:
            return self.getSatClockErrorNav(epoch)
        elif self.source == SP3:
            #TODO
            pass
    
    def getSatPosSP3(self, t, degrees=6):
        #print(np.shape(self.coords))
        #print(self.coords)

        #return Point(coord=self.coords[np.where(self.coords[:,0] == epoch)[0], 1:4], system=ellipsoid.WGS84())
    #def _getSP3Coeffs(self, t,):
        
        #print(self.coords[:,0])
        #timeDiff =np.empty((0,8))
        #for ep in self.coords[:,:]:
        #    a = np.append([ep], [[(ep[0]*604800 + ep[1]) - (t.GPSweek*604800 + t.TOW), ep[0]*604800 + ep[1]]], axis=1)
        #    timeDiff = np.append(timeDiff, a, axis=0)
        
        timeDiff = self.coords[:,:]
        
        timeDiff = np.append(timeDiff, timeDiff[:,6:7] - (t.GPSweek*604800 + t.TOW), axis=1)

        timeDiff = timeDiff[np.abs(timeDiff[:,7]).argsort(), :]
        timeDiff = timeDiff[0:degrees, :]
        timeDiff = timeDiff[np.abs(timeDiff[:,6]).argsort(), :]

        

        alpha = np.ones((degrees,1))

        ep = t.GPSweek*604800 + t.TOW
        #print(timeDiff)
        for i in range(0,degrees):
            for j in range(0, degrees):
                if i == j:continue
                alpha[i,0] = alpha[i,0]*(ep - timeDiff[j,6])/(timeDiff[i,6] - timeDiff[j,6])


        #for i in range(0,degrees):
        interpolated = np.sum(timeDiff[:,2:6]*alpha[:,0:1], axis=0)
        #print(interpolated[3])
        return Point(coord=interpolated[0:3], system=ellipsoid.WGS84()), interpolated[3]/1000000
        #print(np.sum())


        #print(np.append(self.coords[:,0:1],self.coords[:,0:1]-t,axis=1))
        #print(t)
        #self.getSatPos()
            
        
    def getSatPos(self, epoch, degrees=6):
        if self.source == BRDC:
            return self.getSatPosNav(epoch)
        elif self.source == SP3:
            return self.getSatPosSP3(epoch, degrees)
            
            #return self.getSatPosSP3(epoch)





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
    def getSatClockError(self, epoch):
        """get satellite clock error in case of GPS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: clock error of satellite at given epoch (Point)
        """
        ephemerids = self.getValidEph(epoch)

        

        tk = (epoch.GPSweek - ephemerids['GPSWEEK'])*604800 + (epoch.TOW - ephemerids['TOE'])

        return  ephemerids['a0'] + ephemerids['a1']*tk + ephemerids['a2']*tk**2




    def getSatPosNav(self, epoch):
        """get satellite position in case of GPS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        #get valid navigation data to calculate the satellite position

        clk_error = self.getSatClockError(epoch)
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
        return p, clk_error


    @property
    def T1(self):
        return 1/self.f1
    @property
    def T2(self):
        return 1/self.f2
    @property
    def T5(self):
        return 1/self.f5
    
    @property
    def l_ionofree(self):
        return scipy.constants.c/self.f_ionofree
    
    @property
    def f_ionofree(self):
        return self.f1 + self.f2

class GLONASSSat(Satellite):

    freqNum = {
        'R01': 1,
        'R02': -4,
        'R03': 5,
        'R04': 6,
        'R05': 1,
        'R06': -4,
        'R07': 5,
        'R08': 6,
        'R09': -2,
        'R10': -7,
        'R11': 0,
        'R12': -1,
        'R13': -2,
        'R14': -7,
        'R15': 0,
        'R16': -1,
        'R17': 4,
        'R18': -3,
        'R19': 3,
        'R20': 2,
        'R21': 4,
        'R22': -3,
        'R23': 3,
        'R24': 2,
        #'R25': 1,#################x
        #'R26': 1,
        #'R27': 1,
        #'R28': 1,
        #'R29': 1,
        #'R30': 1,

    }



    def __new__(self, prn='', nav={}):
        return object.__new__(self)

    def __init__(self, prn='', nav={}):
        super(GLONASSSat, self).__init__(prn, nav)
        self.diffEqSolved = np.empty((0,8))

    @property
    def f1(self):
        return (1602 + self.freqNum[self.prn]*0.5625)*10**6

    @property
    def f2(self):
        return (1246 + self.freqNum[self.prn]*0.4375)*10**6
    
    @property
    def l_ionofree(self):
        return scipy.constants.c/self.f_ionofree
    
    @property
    def f_ionofree(self):
        return self.f1 + self.f2


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


    def getSatPosNav(self, epoch):
        """get satellite position in case of GLONASS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
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
    f1 = 1575.42*10**6#Hz
    f5 = 1191.795*10**6#Hz
    f5a = 1176.45*10**6#Hz
    f5b = 1207.14*10**6#Hz
    f6 = 1278.750*10**6#Hz

    @property
    def l5a(self):
        return scipy.constants.c/self.f5a
    @property
    def l5b(self):
        return scipy.constants.c/self.f5b
    
    @property
    def l_ionofree(self):
        return scipy.constants.c/self.f_ionofree
    @property
    def l_ionofree_1_5b(self):
        return scipy.constants.c/self.f_ionofree_1_5b
    
    @property
    def f_ionofree_1_5b(self):
        return self.f1 + self.f5b

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
    def getSatClockError(self, epoch):
        """get satellite clock error in case of Galileo satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: clock error of satellite at given epoch (Point)
        """
        ephemerids = self.getValidEph(epoch)

        

        tk = (epoch.GPSweek - ephemerids['GPSWEEK'])*604800 + (epoch.TOW - ephemerids['TOE'])

        return  ephemerids['a0'] + ephemerids['a1']*tk + ephemerids['a2']*tk**2


    def getSatPosNav(self, epoch):
        """get satellite position in case of GPS satellite

                :param epoch: timestamp when we get the position of satellite (Epoch)
                :returns: position of satellite at given epoch (Point)
        """
        #get valid navigation data to calculate the satellite position
        clk_error = self.getSatClockError(epoch)
        t_ref = Epoch()
        t_ref.GPSweekTOW(self.GAGP[3], self.GAGP[2])
        dt = self.GAGP[0] + self.GAGP[1]*(epoch.TOW - t_ref.TOW)
        epoch += Epoch(np.array([0,0,0,0,0,dt]))

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
        return p, clk_error


    @property
    def T1(self):
        return 1/self.f1
    @property
    def T2(self):
        return 1/self.f2
    @property
    def T5(self):
        return 1/self.f5
    @property
    def T5a(self):
        return 1/self.f5a
    @property
    def T5b(self):
        return 1/self.f5b
    @property
    def T6(self):
        return 1/self.f6
