import sys
sys.path.append('./src/')
from rnxreader import RNXReader
from gpsnavreader import GPSNavReader
import math
from epoch import Epoch
import numpy as np
from point import Point
from pointxyz import PointXYZ
from rotation import Rotation
#from station import Station
import math
from iugg67 import IUGG67
obs = RNXReader('61300921A.19o')
#obs.readObservations

pos = PointXYZ(coord = obs.approxPosition)

#plh = pos.getPLH()
#ppp = PointXYZ(coord = np.array([[4103638.79513996], [1327920.20810333],[4683095.51266413]]), system=IUGG67())
#ppp.getPLH()
#r = math.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
#print(r)

gpsnav = GPSNavReader('61300921A.19n')
#gpsnav = GPSNavReader('proba.11n')

sat = gpsnav.getSatellite('G08')

#print(sat.navigationDatas)
satPos = sat.getSatPos(Epoch(np.array([2019,4,2,8,14,59])))
#print(plh.coord[0:2]*180/math.pi)


epochs = sat.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,50,0])))
#print(epochs)
#print(satPos)

#print(sat.navigationDatas[0]['a'])

#satr = math.sqrt(satPos[0,0]**2 + satPos[1,0]**2 + satPos[2,0]**2)
#print(r)
#print(math.sqrt(sat.navigationDatas[0]['a']**2 - sat.navigationDatas[0]['e']**2*sat.navigationDatas[0]['a']**2))
