import sys
sys.path.append('../src/')
import glonassnavreader
import gpsnavreader
import broadcastnavreader
import sp3reader
import epoch
import numpy as np

import matplotlib
import matplotlib.pyplot as plt



gps = gpsnavreader.GPSNavReader('../data/validation/202194/abmf0940.21n')
glo = glonassnavreader.GLONASSNavReader('../data/validation/202194/abmf0940.21g')
gal = broadcastnavreader.BroadcastNavReader('../data/validation/202194/BRDC00WRD_S_20210940000_01D_MN.rnx')

sp3 = sp3reader.SP3Reader('../data/validation/202194/cod21520.eph_r')
diff = {}
for prn in sp3.positions:
    print(prn)
    if prn[0] != 'R':
        continue

    diff[prn] = np.empty((0,7))
    #print(sp3.positions[prn])

    sat = gal.getSatellite(prn)





    for e in sp3.positions[prn]:
        #sat.getSatPos(e[0]).getXYZ().T



        try:
            #print(sat.getSatPos(e[0]))
            #print(np.append([[e[0].MJD]], np.append([e[1:4]], sat.getSatPos(e[0]).getXYZ().T, axis=1), axis=1))
            diff[prn] = np.append(diff[prn], np.append([[e[0].MJD]], np.append([e[1:4]], sat.getSatPos(e[0]).getXYZ().T, axis=1), axis=1), axis=0)
        except epoch.TimeError as er:
            print(er)
            #print('!')
    #print(sat.getSatPos(epoch.Epoch(np.array([2021,4,3,23,59,59.0]))))
for prn in diff:
    print(prn)

    #print(diff[prn])

    fig, axs = plt.subplots(3, 3)

    t = diff[prn][:,0]

    axs[0,0].plot(t, diff[prn][:,1], '-')
    axs[0,0].set(xlabel="t [day]", ylabel='diff X [m]', title=prn)
    axs[1,0].plot(t, diff[prn][:,2], '-')
    axs[1,0].set(xlabel="t [day]", ylabel='diff Y [m]', title=prn)
    axs[2,0].plot(t, diff[prn][:,3], '-')
    axs[2,0].set(xlabel="t [day]", ylabel='diff Z [m]', title=prn)

    axs[0,1].plot(t, diff[prn][:,4], '-')
    axs[0,1].set(xlabel="t [day]", ylabel='diff X [m]', title=prn)
    axs[1,1].plot(t, diff[prn][:,5], '-')
    axs[1,1].set(xlabel="t [day]", ylabel='diff Y [m]', title=prn)
    axs[2,1].plot(t, diff[prn][:,6], '-')
    axs[2,1].set(xlabel="t [day]", ylabel='diff Z [m]', title=prn)

    axs[0,2].plot(t, diff[prn][:,1] - diff[prn][:,4], '-')
    axs[0,2].set(xlabel="t [day]", ylabel='diff X [m]', title=prn)
    axs[1,2].plot(t, diff[prn][:,2] - diff[prn][:,5], '-')
    axs[1,2].set(xlabel="t [day]", ylabel='diff Y [m]', title=prn)
    axs[2,2].plot(t, diff[prn][:,3] - diff[prn][:,6], '-')
    axs[2,2].set(xlabel="t [day]", ylabel='diff Z [m]', title=prn)

    plt.show()
