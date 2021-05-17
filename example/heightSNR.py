import sys
sys.path.append('../src/')
from rnxreader import RNXReader
from gpsnavreader import GPSNavReader
from glonassnavreader import GLONASSNavReader
import math
from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from point import Point
import matplotlib
import matplotlib.pyplot as plt
import scipy.signal as signal
from lsfrequency import lsfrequency
import ellipsoid
obs = RNXReader('61300921A.19o')

navs = GPSNavReader('brdc0920.19n')

#obs = RNXReader('../data/118/mini.19o')
obs.readObservations();

#navs = GPSNavReader('../data/118/brdc118_v2.19N')
navsglo = GLONASSNavReader('brdc0920.19g')





#s.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
obsTypes = ('S1','S2')
sats = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
        'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19',
        'G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29',
        'G31', 'G32', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
        'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17',
        'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26',
        'R27', 'R28', 'R29', 'R30', 'R31', 'R32', 'R33', 'R34')

sats = ('G17', )
observations = obs.getObservations(sats=sats, obsTypes=obsTypes)


elevAzMask = np.array([[0, 40],[0, 360]])*np.pi/180

SNR = {}
for prn in observations:
    for t in range(len(obsTypes)):
        SNR[obsTypes[t]] = np.empty((0,2))
        SNR[obsTypes[t]] = np.empty((0,2))

    if prn[0] == 'G':
        s = navs.getSatellite(prn)
    elif prn[0] == 'R':
        s = navsglo.getSatellite(prn)


    for i in observations[prn]:
        #print(i[1:3])

        try:
            elevAz = s.getElevAzimuth(Point(coord = obs.approxPosition, system=ellipsoid.WGS84()), i[0])
            #print(elevAz[1]*180/np.pi)
            if elevAzMask[0,0] <= elevAz[0] <= elevAzMask[0,1] and elevAzMask[1,0] <= elevAz[1] <= elevAzMask[1,1]:
                for t in range(len(obsTypes)):
                    a = np.append(elevAz[0], i[t+1])
                    #if i[t+1] != 0:
                    SNR[obsTypes[t]] = np.append(SNR[obsTypes[t]], [a], axis=0)
            #if i[1] == 0 or i[2] == 0:
            #    print(a)
            #
        except TimeError:

            print(i[0])
    #print(np.shape(SNR))
    #
    print(SNR[obsTypes[t]])

    sine = {}
    f = {}
    p = {}
    trend = {}
    residuals = {}
    periodogram = {}
    maxi = {}
    show = False
    print(prn)
    print(np.shape(SNR[obsTypes[t]]))
    for t in range(len(obsTypes)):
        if np.shape(SNR[obsTypes[t]]) == (0,2):
            continue
        show = True
    if show:
        fig, axs = plt.subplots(2, len(obsTypes))

    for t in range(len(obsTypes)):
        if np.shape(SNR[obsTypes[t]]) == (0,2):
            continue
        show = True
        sine[obsTypes[t]] = np.sin(SNR[obsTypes[t]][:,0])
        #print(sine)
        SNR[obsTypes[t]][:,1] = 10**(SNR[obsTypes[t]][:,1]/20)

        l = eval("s.l"+obsTypes[t][1])
        print(l)

        f[obsTypes[t]] = lsfrequency(l, 5, 30, 0.01)

        p[obsTypes[t]] = np.poly1d(np.polyfit(sine[obsTypes[t]], SNR[obsTypes[t]][:,1], 2))
        trend[obsTypes[t]] = p[obsTypes[t]](sine[obsTypes[t]])
        residuals[obsTypes[t]] = SNR[obsTypes[t]][:,1] - trend[obsTypes[t]]
        periodogram[obsTypes[t]] = signal.lombscargle(sine[obsTypes[t]], residuals[obsTypes[t]], f[obsTypes[t]])
        maxi[obsTypes[t]] = np.argmax(periodogram[obsTypes[t]])





        axs[0,t].plot(sine[obsTypes[t]], SNR[obsTypes[t]][:,1], '-', sine[obsTypes[t]], trend[obsTypes[t]], '--')
        axs[0,t].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values ' + obsTypes[t])



        #h


        axs[1,t].plot(f[obsTypes[t]]*l/(4*math.pi), periodogram[obsTypes[t]], '-', f[obsTypes[t]][maxi[obsTypes[t]]]*l/(4*math.pi), periodogram[obsTypes[t]][maxi[obsTypes[t]]], 'o')
        axs[1,t].set(xlabel="f", ylabel='aaaa', title='Periodogram values' + prn)

        print(f[obsTypes[t]][maxi[obsTypes[t]]]*l/(4*math.pi))

        #axs[0,t].plot(sine2, SNR2[:,1], '-', sine2, trend2, '--')
        #axs[0,t].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values G25')



        #axs[1,t].plot(f2*s.l2/(4*math.pi), periodogram2, '-', f2[maxi2]*s.l2/(4*math.pi), periodogram2[maxi2], 'o')
        #axs[1,t].set(xlabel="f", ylabel='aaaa', title='Periodogram values G25')

    if show:
        plt.show()
