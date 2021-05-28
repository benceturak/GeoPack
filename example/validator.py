import sys
sys.path.append('../src/')
import glonassnavreader
import gpsnavreader
import sp3reader
import epoch
import numpy as np



gps = gpsnavreader.GPSNavReader('../data/validation/202194/abmf0940.21n')
glo = glonassnavreader.GLONASSNavReader('../data/validation/202194/abmf0940.21g')
sp3 = sp3reader.SP3Reader('../data/validation/202194/cod21520.eph_r')
diff = {}
for prn in sp3.positions:

    diff[prn] = np.empty((0,4))
    #print(sp3.positions[prn])
    if prn[0] == 'G':
        continue
        sat = gps.getSatellite(prn)
    elif prn[0] == 'R':
        sat = glo.getSatellite(prn)

    for e in sp3.positions[prn]:

        try:

            diff[prn] = np.append(diff[prn], np.append([[e[0]]], e[1:4] - sat.getSatPos(e[0]).getXYZ().T, axis=1), axis=0)
        except:
            pass
            #print('!')
    print(prn)
    print(diff[prn])
    print('---------------------------')
    #print(sat.getSatPos(epoch.Epoch(np.array([2021,4,3,23,59,59.0]))))
