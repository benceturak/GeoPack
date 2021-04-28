import sys
sys.path.append('../src/')
from rnxreader import RNXReader
from gpsnavreader import GPSNavReader
import math
from epoch import Epoch
from epoch import TimeError
import numpy as np
import math
from wgs84 import WGS84
from point import Point
import matplotlib
import matplotlib.pyplot as plt
import scipy.signal as signal
from lsfrequency import lsfrequency


obs = RNXReader('../data/118/mini.19o')
obs.readObservations();

sats = GPSNavReader('../data/118/brdc118_v2.19N')

s = sats.getSatellite('G25')


#s.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,0,1.0])))
SNR17 = obs.getObservations('G25', 'S1')

SNR = np.empty((0,2))

for i in SNR17:

    try:
        elevAz = s.getElevAzimuth(Point(coord = obs.approxPosition, system=WGS84()), i[0])
        a = np.append(i[1], elevAz[0])
        SNR = np.append(SNR, [a], axis=0)
    except TimeError:
        pass
sine = np.sin(SNR[:,1])
SNR[:,1] = 10**(SNR[:,0]/20)

f = lsfrequency(s.l1, 5, 30, 0.01)

p = np.poly1d(np.polyfit(sine, SNR[:,0], 2))

trend = p(sine)

residuals = SNR[:,0] - trend

periodogram = signal.lombscargle(sine, residuals, f)

fig, axs = plt.subplots(2, 1)
axs[0].plot(sine, SNR[:,0], '-', sine, trend, '--')
axs[0].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values G25')

axs[1].plot(f*s.l1/(4*math.pi), periodogram)
axs[1].set(xlabel="f", ylabel='aaaa', title='Periodogram values G25')


plt.show()
