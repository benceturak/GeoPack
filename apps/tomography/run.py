import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import broadcastnavreader
import readcrd
import readtrp
import orographyreader
import epoch
import numpy as np
from scipy import stats
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
from plotregression import plotRegression

RS = [
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1100.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1100.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1100.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1112.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1112.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1112.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']],
[['Budapest','12843', station.Station(coord=np.array([47.43*np.pi/180,19.18*np.pi/180,139.0]), type=2, system=WGS84()), 'BP_1200.csv'],
['Szeged', '12982', station.Station(coord=np.array([46.25*np.pi/180,20.10*np.pi/180,84.0]), type=2, system=WGS84()), 'SZ_1200.csv'],
['Popgrad', '11952', station.Station(coord=np.array([49.03*np.pi/180,20.32*np.pi/180,701.0]), type=2, system=WGS84()), 'PO_1200.csv']]

]



code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

source_dir = '../../data/tomography/2021/'
output_dir = '../../data/tomography/2021/result/'



constellations = 'TRPGG/'

output_file = constellations+'CT_'

gridp = np.loadtxt('gridp.csv')*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt('gridl.csv')*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt('gridh.csv')


x0_3D = np.load(source_dir+'initial.npy')





eps = np.array([epoch.Epoch(np.array([2021,8,11,0,0,0]), epoch.GPS)])
dep = epoch.Epoch(np.array([0,0,0,1,0,0]))

for i in range(0,23):
    eps = np.append(eps, eps[-1]+dep)


#input files

#station coordinate file CRD
station_coords = source_dir+'METEONET.CRD'
#troposphere files


#VMF1 grid file
vmf1_grid = [source_dir+'GRD/VMFG_20210811.H00',source_dir+'GRD/VMFG_20210811.H06',source_dir+'GRD/VMFG_20210811.H12',source_dir+'GRD/VMFG_20210811.H18',source_dir+'GRD/VMFG_20210812.H00']
orography_ell = source_dir+'orography_ell'
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_R_20212230000_01D_MN.rnx'
#epoch of the calculation

network = readcrd.ReadCRD(station_coords).network
brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)

for sat in brdc.getSatellites():
    network.addSatellite(sat)


orography = orographyreader.OrographyReader(orography_ell)

grid = vmf1gridreader.VMF1GridReader(vmf1_grid, orography)
mapping_function = vmf1.VMF1(grid)

x0_t = np.empty((0,))
for i in range(0, np.shape(gridh)[0]-1):
    x0_t = np.append(x0_t, (gridh[i] + gridh[i+1])/2)

cellX = len(gridp)-1
cellY = len(gridl)-1
cellZ = len(gridh)-1

for ep in eps:
    print(ep)
    print(ep.GPS[3])
    c = code_letter[ep.GPS[3]]
    filename = output_dir+output_file+str(ep.DOY)+c
    print(filename)


    bernese_tropo = source_dir+constellations+'CR21'+str(ep.DOY)+c+'.TRP'


    tropo = readtrp.ReadTRP(bernese_tropo)

    x0 = matrix2vector(x0_3D)

    A, b, stations = tomography(gridp, gridl, gridh, network, tropo, mapping_function, ep, ('G','R'), ())






    numOfRay = len(b)
    R = np.random.permutation(numOfRay)
    train_rate = int(numOfRay*0.8)

    train_A = A[R[0:train_rate]]
    train_b = b[R[0:train_rate]]

    test_A = A[R[train_rate:]]
    test_b = b[R[train_rate:]]




    while True:
        Nw_vec, iter_num = mart.mart(train_A, train_b, 3000, x0, 2.7/100)

        train_b_est = np.dot(train_A, Nw_vec)*10**-6


        m, section, r, p, se = stats.linregress(train_b*10**-6, train_b_est)

        regline = lambda x: m*x + section

        diff = train_b_est - regline(train_b*10**-6)

        sigma = float(np.std(diff))

        numOfRay = len(train_b_est)

        print(np.shape(train_A))

        indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
        train_A = train_A[indeces,:]
        print(np.shape(train_A))
        train_b = train_b[indeces]

        train_b_est = train_b_est[indeces]
        #stations = stations[np.where(np.abs(diff) < 3*np.std(diff))]
        print(sigma*3)
        print(diff[np.where(np.abs(diff) > 3*np.std(diff))[0]])

        if numOfRay == len(train_b_est):
            break

    test_b_est = np.dot(test_A, Nw_vec)*10**-6

    train_b_init = np.dot(train_A, x0)*10**-6
    test_b_init = np.dot(test_A, x0)*10**-6


    plotRegression(train_b_est, train_b*10**-6, output_dir+constellations+"regression/regression_train_estimated_"+str(ep.DOY)+c+".png", "Regression train estimated:", ep, sigma)
    plotRegression(test_b_est, test_b*10**-6, output_dir+constellations+"regression/regression_test_estimated_"+str(ep.DOY)+c+".png", "Regression test estimated:", ep)

    plotRegression(train_b_init, train_b*10**-6, output_dir+constellations+"regression/regression_train_initial_"+str(ep.DOY)+c+".png", "Regression train initial:", ep)
    plotRegression(test_b_init, test_b*10**-6, output_dir+constellations+"regression/regression_test_initial_"+str(ep.DOY)+c+".png", "Regression test initial:", ep)


    stats_row = [[ep.UTC[3], len(b), int(len(b)*0.8), numOfRay, sigma, iter_num]]
    try:
        statistic = np.append(statistic, stats_row, axis=0)
    except:
        statistic = np.array(stats_row)

    #np.savetxt(output_dir+constellations+"", res['x'], delimiter=",")



    Nw_3D = vector2matrix(Nw_vec, (cellX, cellY, cellZ))



    np.save(filename+'.npy',Nw_3D)
    #np.save(source_dir+'initial.npy', x0_3D )
    np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    plotRefractivity(filename+'.png', Nw_3D, ep)


    for sonde in RS[ep.GPS[3]]:
        print()
        print(sonde[3])


        sta = sonde[2]

        rs = np.loadtxt(source_dir+'RS/'+sonde[3], delimiter=',')

        rs = rs[np.where(rs[:,0] <= 10000)[0],:]
        rs = rs[:,[0,1]]

        tomo_profile = getProfileFromCT(Nw_3D, gridp, gridl, sta, 'bilinear')

        initial_profile = getProfileFromCT(x0_3D, gridp, gridl, sta)



        tomo = np.append([x0_t], [tomo_profile], axis=0).T
        initial = np.append([x0_t], [initial_profile], axis=0).T

        refractivityProfile(('Initial', 'Tomography', 'Radiosonde'), (initial, tomo, rs), sonde[0], output_dir+constellations+'profile_'+sonde[0]+'_'+str(ep.DOY)+c+'.png', ep)
np.savetxt(output_dir+constellations+"stats.csv", statistic, delimiter=",")
    #x0_3D = res[0]
