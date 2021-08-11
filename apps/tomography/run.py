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
import station
from ellipsoid import WGS84
from getprofilefromct import getProfileFromCT
from refractivityprofile import refractivityProfile

RS = [
['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']]



code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

source_dir = '../../data/tomography/2021/'
output_dir = '../../data/tomography/2021/result/'



constellations = 'TRP/'

output_file = constellations+'CT_'

gridp = np.loadtxt('gridp.csv')*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt('gridl.csv')*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt('gridh.csv')


x0_3D = np.load(source_dir+'initial.npy')





eps = np.array([epoch.Epoch(np.array([2021,8,11,2,0,0]), epoch.UTC)])
dep = epoch.Epoch(np.array([0,0,0,1,0,0]))

for i in range(0,5):
    eps = np.append(eps, eps[-1]+dep)


#input files

#station coordinate file CRD
station_coords = source_dir+'SO21196A.CRD'
#troposphere files


#VMF1 grid file
vmf1_grid = [source_dir+'GRD/VMFG_20210811.H00',source_dir+'GRD/VMFG_20210811.H06']#,source_dir+'GRD/VMFG_20210811.H12',source_dir+'GRD/VMFG_20210811.H18',source_dir+'GRD/VMFG_20210812.H00']
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_S_20212230000_01D_MN.rnx'
#epoch of the calculation

network = readcrd.ReadCRD(station_coords).network
brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)

for sat in brdc.getSatellites():
    network.addSatellite(sat)


grid = vmf1gridreader.VMF1GridReader(vmf1_grid)
mapping_function = vmf1.VMF1(grid)

x0_t = np.empty((0,))
for i in range(0, np.shape(gridh)[0]-1):
    x0_t = np.append(x0_t, (gridh[i] + gridh[i+1])/2)

for ep in eps:
    c = code_letter[ep.UTC[3]]
    filename = output_dir+output_file+c
    print(filename)


    bernese_tropo = source_dir+constellations+'CO21223'+c+'.TRP'


    tropo = readtrp.ReadTRP(bernese_tropo)

    x0 = matrix2vector(x0_3D)
    res = tomography(gridp, gridl, gridh, network, tropo, grid, mapping_function, x0, ep, ('G','R','E'))
    T = res[0]

    np.save(filename+'.npy',res[0])
    #np.save(source_dir+'initial.npy', x0_3D )
    np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    plotRefractivity(filename+'.png', res[0])


    for sonde in RS:


        sta = sonde[2]

        rs = np.loadtxt(source_dir+'RS/'+sonde[3], delimiter=',')

        rs = rs[np.where(rs[:,0] <= 10000)[0],:]
        rs = rs[:,[0,1]]

        tomo_profile = getProfileFromCT(res[0], gridp, gridl, sta)

        initial_profile = getProfileFromCT(x0_3D, gridp, gridl, sta)

        tomo = np.append([x0_t], [tomo_profile], axis=0).T
        initial = np.append([x0_t], [initial_profile], axis=0).T

        refractivityProfile(('Initial', 'Tomography', 'Radiosonde'), (initial, tomo, rs), sonde[0], output_dir+constellations+'profile_'+sonde[0]+'_'+c+'.png')

    #x0_3D = res[0]
