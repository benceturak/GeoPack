import sys
sys.path.append('../src/')
from rnxreader import RNXReader
from gpsnavreader import GPSNavReader
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
#obs = RNXReader('mini.19o')

#sats = GPSNavReader('61300921A.19n')

obs = RNXReader('../data/118/mini.19o')
obs.readObservations();

sats = GPSNavReader('../data/118/brdc118_v2.19N')




#s.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
observations = obs.getObservations(sats=('G25','G26','G27'), obsTypes=('S1','S2'))


elevAzMask = np.array([[0, 25],[170, 180]])*np.pi/180

for prn in observations:
    SNR = np.empty((0,3))

    s = sats.getSatellite(prn)


    for i in observations[prn]:
        #print(i[1:3])

        try:
            elevAz = s.getElevAzimuth(Point(coord = obs.approxPosition, system=ellipsoid.WGS84()), i[0])
            a = np.append(elevAz[0], i[1])
            a = np.append(a, i[2])
            SNR = np.append(SNR, [a], axis=0)

            #
        except TimeError:
            print(i[0])
    print(np.shape(SNR))


    sine = np.sin(SNR[:,0])
    #print(sine)
    SNR[:,1] = 10**(SNR[:,1]/20)
    SNR[:,2] = 10**(SNR[:,2]/20)

    f1 = lsfrequency(s.l1, 5, 30, 0.01)

    p1 = np.poly1d(np.polyfit(sine, SNR[:,1], 2))
    trend1 = p1(sine)
    residuals1 = SNR[:,1] - trend1
    periodogram1 = signal.lombscargle(sine, residuals1, f1)
    maxi1 = np.argmax(periodogram1)

    f2 = lsfrequency(s.l2, 5, 30, 0.01)
    p2 = np.poly1d(np.polyfit(sine, SNR[:,2], 2))
    trend2 = p2(sine)
    residuals2 = SNR[:,2] - trend2
    periodogram2 = signal.lombscargle(sine, residuals2, f2)
    maxi2 = np.argmax(periodogram2)


    fig, axs = plt.subplots(2, 2)
    axs[0,0].plot(sine, SNR[:,1], '-', sine, trend1, '--')
    axs[0,0].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values G25')



    axs[1,0].plot(f1*s.l1/(4*math.pi), periodogram1, '-', f1[maxi1]*s.l1/(4*math.pi), periodogram1[maxi1], 'o')
    axs[1,0].set(xlabel="f", ylabel='aaaa', title='Periodogram values G25')

    axs[0,1].plot(sine, SNR[:,2], '-', sine, trend2, '--')
    axs[0,1].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values G25')



    axs[1,1].plot(f2*s.l2/(4*math.pi), periodogram2, '-', f2[maxi2]*s.l2/(4*math.pi), periodogram2[maxi2], 'o')
    axs[1,1].set(xlabel="f", ylabel='aaaa', title='Periodogram values G25')


    plt.show()
