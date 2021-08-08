import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import readcrd
import numpy as np
import matplotlib.pyplot as plt
import mplleaflet
import station
from ellipsoid import WGS84

code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

gridp = np.loadtxt('gridp.csv')#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt('gridl.csv')#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt('gridh.csv')
RS = [
['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84())],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84())],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84())]]


#input files
source_dir = '../../data/tomography/2021/'
#station coordinate file CRD
station_coords = source_dir+'SO21196A.CRD'
#troposphere files



network = readcrd.ReadCRD(station_coords).network

stations =  network.getStationsMatrix()['coords'][:,0:2]*180/np.pi




fig, axs = plt.subplots()
axs.set(xlabel="Refractivity [-]", ylabel='height [m]', title='Stations')


for sta in stations:
    if gridp[0] <= sta[0] <= gridp[-1] and gridl[0] <= sta[1] <= gridl[-1]:
        axs.plot(sta[1], sta[0], 'ro', markersize=10,label='GNSS stations')

for rs in RS:
    rs_coords = rs[2].getPLH()[0:2,0]*180/np.pi
    axs.plot(rs_coords[1], rs_coords[0], 'bP', markersize=16,label='Radiosonde stations')


for p in gridp:
    axs.plot((gridl[0], gridl[-1]), (p,p), 'b-')

for l in gridl:
    axs.plot((l,l), (gridp[0], gridp[-1]), 'b-')



mplleaflet.show()
