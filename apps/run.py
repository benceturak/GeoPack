import sys
sys.path.append('../src/')
from rnxreader import RNXReader
from gpsnavreader import GPSNavReader
import math
from epoch import Epoch
import numpy as np
from point import Point
from point import XYZ, PLH
from rotation import Rotation
#from station import Station
import math
from iugg67 import IUGG67
from wgs84 import WGS84
obs = RNXReader('61300921A.19o')
#obs.readObservations

pos = Point(coord = obs.approxPosition, system=WGS84())

#plh = pos.getPLH()
#ppp = PointXYZ(coord = np.array([[4103638.79513996], [1327920.20810333],[4683095.51266413]]), system=IUGG67())
#ppp.getPLH()
#r = math.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)

gpsnav = GPSNavReader('61300921A.19n')
#gpsnav = GPSNavReader('proba.11n')

sat = gpsnav.getSatellite('G08')
#pos = Point(coord=np.array([(47+28/60+51.39741/3600)*math.pi/180, (19+3/60+23.50703/3600)*math.pi/180, 180.798]), type=PLH, system=WGS84())


#print(sat.navigationDatas)
#satPos = sat.getSatPos(Epoch(np.array([2019,4,2,8,14,59])))
print(sat.getElevAzimuth(pos, Epoch(np.array([2019,4,2,7,29,59])))*180/math.pi)
print(sat.getElevAzimuth(pos, Epoch(np.array([2019,4,2,7,44,59])))*180/math.pi)
print(sat.getElevAzimuth(pos, Epoch(np.array([2019,4,2,7,59,59])))*180/math.pi)
print(sat.getElevAzimuth(pos, Epoch(np.array([2019,4,2,8,14,59])))*180/math.pi)
print(sat.getElevAzimuth(pos, Epoch(np.array([2019,4,2,8,29,59])))*180/math.pi)
#print(sat.getElevAzimuth(pos, Epoch(np.array([2011,3,31,8,14,59])))*180/math.pi)

#epochs = sat.getEpochsInValidTimeFrame(Epoch(np.array([0,0,0,0,50,0])))
#print(epochs)
#print(satPos)

#print(sat.navigationDatas[0]['a'])

#satr = math.sqrt(satPos[0,0]**2 + satPos[1,0]**2 + satPos[2,0]**2)
#print(r)
#print(math.sqrt(sat.navigationDatas[0]['a']**2 - sat.navigationDatas[0]['e']**2*sat.navigationDatas[0]['a']**2))
