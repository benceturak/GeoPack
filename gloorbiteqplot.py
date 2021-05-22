import sys
sys.path.append('src/')
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
import ellipsoid

nav = GLONASSNavReader('example/61300921A.19g')
sat = nav.getSatellite('R16')

sol = sat.getSatPos(Epoch(np.array([2019, 4, 2, 7, 38, 42.0])))
print(sol)
#t0 = np.argmin(np.abs(sol.t))

#print(sol['y'][0,t0])
#print(sol['y'][1,t0])
#print(sol['y'][2,t0])
#print(sol['y'][3,t0])
#print(sol['y'][4,t0])
#print(sol['y'][5,t0])

#fig, axs = plt.subplots(2, 1)

#axs[0].plot(sol.t, sol['y'][0,:], '*', sol.t, sol['y'][1,:], '*',sol.t, sol['y'][2,:],'*')
#axs[0,0].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values ' + obsTypes[t])

#axs[1].plot(sol.t, sol['y'][3,:], '*', sol.t, sol['y'][4,:], '*',sol.t, sol['y'][5,:],'*')
#axs[1,0].set(xlabel="sin(e) [-]", ylabel='SNR [volts/volts]', title='SNR values ' + obsTypes[t])
#plt.show()
