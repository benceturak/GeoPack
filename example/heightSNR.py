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
fig, ax = plt.subplots()
ax.plot(sine, SNR[:,0])
ax.set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values G17')
ax.grid()

plt.show()
