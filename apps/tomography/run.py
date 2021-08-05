import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import broadcastnavreader
import readcrd
import readtrp
import epoch
import numpy as np
import vmf1gridreader
import vmf1
import mart
from plotrefractivity import plotRefractivity
from vector2matrix import vector2matrix
from matrix2vector import matrix2vector
from tomography import tomography
import matplotlib.pyplot as plt


code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

gridp = np.loadtxt('gridp.csv')*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt('gridl.csv')*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt('gridh.csv')

ccc = int((np.shape(gridp)[0]-1)*(np.shape(gridl)[0]-1)*(np.shape(gridh)[0]-1)/6)
x0_3D = np.zeros((len(gridp)-1, len(gridl)-1, len(gridh)-1))

x0_3D[:,:,0] = np.ones((len(gridp)-1, len(gridl)-1))*72.4628
x0_3D[:,:,1] = np.ones((len(gridp)-1, len(gridl)-1))*58.6927
x0_3D[:,:,2] = np.ones((len(gridp)-1, len(gridl)-1))*48.5702
x0_3D[:,:,3] = np.ones((len(gridp)-1, len(gridl)-1))*25.3141
x0_3D[:,:,4] = np.ones((len(gridp)-1, len(gridl)-1))* 6.6281
x0_3D[:,:,5] = np.ones((len(gridp)-1, len(gridl)-1))* 0.2337



x0 = matrix2vector(x0_3D)

np.savetxt("x0.csv", x0)
eps = np.array([epoch.Epoch(np.array([2021,7,15,0,0,0]), epoch.UTC)])
dep = epoch.Epoch(np.array([0,0,0,1,0,0]))

for i in range(0,23):
    eps = np.append(eps, eps[-1]+dep)


#input files
source_dir = '../../data/tomography/2021/'
#station coordinate file CRD
station_coords = source_dir+'SO21196A.CRD'
#troposphere files


#VMF1 grid file
vmf1_grid = [source_dir+'GRD/VMFG_20210715.H00',source_dir+'GRD/VMFG_20210715.H06',source_dir+'GRD/VMFG_20210715.H12',source_dir+'GRD/VMFG_20210715.H18',source_dir+'GRD/VMFG_20210716.H00']
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_R_20211960000_01D_MN.rnx'
#epoch of the calculation

network = readcrd.ReadCRD(station_coords).network
brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)

for sat in brdc.getSatellites():
    network.addSatellite(sat)


grid = vmf1gridreader.VMF1GridReader(vmf1_grid)
mapping_function = vmf1.VMF1(grid)

for ep in eps:
    c = code_letter[ep.UTC[3]]
    print(c)


    bernese_tropo = source_dir+'TRP/CO21196'+c+'.TRP'


    tropo = readtrp.ReadTRP(bernese_tropo)


    res = tomography(gridp, gridl, gridh, network, tropo, grid, mapping_function, x0, ep)
    T = res[0]
    print(np.shape(T))
    print(T[:,:,0])
    print(T[:,:,1])
    print(T[:,:,2])
    print(T[:,:,3])
    print(T[:,:,4])
    print(T[:,:,5])

    np.save('TTT_'+c+'.npy',res[0])

    x0 = res[1]

    plotRefractivity('TTT_'+c+'.png', res[0])
    exit()
