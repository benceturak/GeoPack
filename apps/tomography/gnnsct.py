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






x0 = matrix2vector(x0_3D)

class GNSSCT(object):

    def __init__(self, gridp, gridl, gridh, x0_3D, network, troposphere, mapping_function, ep, constellation=('G', 'R', 'E'), max_iter=3000, tolerance=2.7):
        self.gridp = gridp
        self.gridl = gridl
        self.gridh = gridh

        self.cellX = len(self.gridp)-1
        self.cellY = len(self.gridl)-1
        self.cellZ = len(self.gridh)-1


        self.x0_3D = np.load(initial_vals_file)

        self.network = network

        self.ep = ep

        self.mapping_function = mapping_function

        self.constellation = constellation

        self.max_iter = max_iter
        self.tolerance = tolerance

    def run(self):

        train_A, train_b, stations = tomography(self.gridp, self.gridl, self.gridh, self.network, self.troposphere, self.mapping_function, self.ep, self.constellation, ())

        while True:
            Nw_vec, iter_num = mart.mart(train_A, train_b, self.max_iter, x0, self.tolerance/100)

            train_b_est = np.dot(train_A, Nw_vec)*10**-6


            m, section, r, p, se = stats.linregress(train_b*10**-6, train_b_est)

            regline = lambda x: m*x + section

            diff = train_b_est - regline(train_b*10**-6)

            sigma = float(np.std(diff))

            numOfRay = len(train_b_est)


            indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
            train_A = train_A[indeces,:])
            train_b = train_b[indeces]

            train_b_est = train_b_est[indeces]


            if numOfRay == len(train_b_est):
                break

        self.Nw_3D = vector2matrix(Nw_vec, (cellX, cellY, cellZ))


if __name__ == "__main__":

    gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
    gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
    gridh = np.loadtxt(gridh_file)


    x0_3D = np.load(initial_vals_file)

    ep = epoch.Epoch(np.array([2021,8,11,6,0,0]), epoch.UTC)

    network = readcrd.ReadCRD(station_coords).network
    brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)

    for sat in brdc.getSatellites():
        network.addSatellite(sat)

    orography = orographyreader.OrographyReader(orography_ell)

    grid = vmf1gridreader.VMF1GridReader(vmf1_grid, orography)
    mapping_function = vmf1.VMF1(grid)



    tropo = readtrp.ReadTRP(bernese_tropo)

    ct = GNSSCT(gridp, gridl, gridh, x0_3D, network, troposphere, mapping_function, ep)




    np.save(filename+'.npy',Nw_3D)
    #np.save(source_dir+'initial.npy', x0_3D )
    np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    plotRefractivity(filename+'.png', Nw_3D)

    #x0_3D = res[0]
