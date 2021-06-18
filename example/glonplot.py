import sys
sys.path.append('../src/')
import glonassnavreader
import gpsnavreader
import sp3reader
import epoch
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt



gps = gpsnavreader.GPSNavReader('../data/validation/202194/abmf0940.21n')
glo = glonassnavreader.GLONASSNavReader('../data/validation/202194/abmf0940.21g')
sp3 = sp3reader.SP3Reader('../data/validation/202194/cod21520.eph_r')

prn = 'R01'

orbitBroadcast = glo.getSatellite(prn)
#orbitBroadcast = gps.getSatellite(prn)

precise = sp3.positions[prn]
pret = np.empty((1,0))
for i in precise[:,0]:
    pret = np.append(pret, i.MJD - math.floor(i.MJD))
year = 2021
month = 4
day = 4
hour = 0
min = 0
sec = 0

startEpoch = epoch.Epoch(np.array([year, month, day, hour, min, sec]))
epdif = epoch.Epoch(np.array([0,0,0,0,1,0]))
endEpoch = epoch.Epoch(np.array([year, month, day, hour, min, sec])) + epoch.Epoch(np.array([0,0,1,0,0,0]))
#print(startEpoch)
#print(endEpoch)
ep = startEpoch
#print(precise)
X = np.empty((1,0))
Y = np.empty((1,0))
Z = np.empty((1,0))
t = np.empty((1,0))

spt = np.empty((1,0))
spx = np.empty((1,0))
spy = np.empty((1,0))
spz = np.empty((1,0))

difx = np.empty((1,0))
dify = np.empty((1,0))
difz = np.empty((1,0))

#pos1 = orbitBroadcast.getSatPos(epoch.Epoch(np.array([2021, 4, 4, 15, 45, 18])))
#print(pos1)
#pos2 = orbitBroadcast.getSatPos(epoch.Epoch(np.array([2021, 4, 4, 15, 44, 42])))
#print(pos2)
#print(pos1-pos2)
while ep < endEpoch:
    #print(ep)
    try:
        pos = orbitBroadcast.getSatPos(ep+epoch.Epoch(np.array([0,0,0,0,0,0])))

        X = np.append(X, pos.xyz[0,0])
        Y = np.append(Y, pos.xyz[1,0])
        Z = np.append(Z, pos.xyz[2,0])
        t = np.append(t, (ep.MJD - math.floor(ep.MJD)))
        #print(np.shape(t))
        try:
            p = precise[np.where(precise[:,0] == ep)]

            #print(spt)
            spx = np.append(spx,p[0,1])
            spy = np.append(spy,p[0,2])
            spz = np.append(spz,p[0,3])
            difx = np.append(difx, pos.xyz[0,0] - p[0,1])
            dify = np.append(dify, pos.xyz[1,0] - p[0,2])
            difz = np.append(difz, pos.xyz[2,0] - p[0,3])

            spt = np.append(spt, (ep.MJD - math.floor(ep.MJD)))
        except:
            pass

        #print(np.shape(difx))
        #print(np.shape(X))
    except:
        #print(ep)
        #X = np.append(X, 0)
        #Y = np.append(Y, 0)
        #Z = np.append(Z, 0)
        #t = np.append(t, ep.MJD - math.floor(ep.MJD))
        #difx = np.append(difx, 0)
        #dify = np.append(dify, 0)
        #difz = np.append(dify, 0)
        pass
        #print(ep)
    ep = ep + epdif

fig, axs = plt.subplots(3, 2)
t = t*24
spt = spt*24
pret = pret*24

#difx = X
#dify = Y
#difz = Z
#print(precise)

#difx[np.where(X == 0)] = 0
#dify[np.where(Y == 0)] = 0
#difz[np.where(Z == 0)] = 0

#print(np.append(np.append([t], [difx], axis=0), [X], axis=0).T)
print(difx)
print(dify)
print(difz)

axs[0,0].plot(t, X, '-', spt, spx, '.')
axs[0,0].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')
axs[1,0].plot(t, Y, '-', spt, spy, '.')
axs[1,0].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')
axs[2,0].plot(t, Z, '-', spt, spz, '.')
axs[2,0].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')

axs[0,1].plot(spt, difx, '*')
axs[0,1].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')
axs[1,1].plot(spt, dify, '*')
axs[1,1].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')
axs[2,1].plot(spt, difz, '*')
axs[2,1].set(xlabel="t [day]", ylabel='X [m]', title='X coords ')
plt.show()
