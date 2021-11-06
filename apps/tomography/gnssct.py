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

        self.troposphere = troposphere

        self.ep = ep

        self.mapping_function = mapping_function

        self.constellation = constellation

        self.max_iter = max_iter
        self.tolerance = tolerance

        self.Nw_3D = None

    def _calcGridCoords(self):

        p = np.empty((0,))
        for i in range(1,np.shape(self.gridp)[0]):
            p = np.append(p, (self.gridp[i-1]+self.gridp[i])/2)
        l = np.empty((0,))
        for i in range(1,np.shape(self.gridl)[0]):
            l = np.append(l, (self.gridl[i-1]+self.gridl[i])/2)
        h = np.empty((0,))
        for i in range(1,np.shape(self.gridh)[0]):
            h = np.append(h, (self.gridh[i-1]+self.gridh[i])/2)
        return (p*180/np.pi,l*180/np.pi,h)




    def writeN2DB(self, database, table):
        cursor = database.cursor()
        sql = 'INSERT INTO ' + table + ' (DATE, TIME, LAT, LON, ALT, NW) VALUES (%s, %s, %s, %s, %s, %s)'
        params = []
        p,l,h = ct._calcGridCoords()


        for i in range(0,np.shape(p)[0]):
            for j in range(0,np.shape(l)[0]):
                for k in range(0,np.shape(h)[0]):
                    params.append((self.ep.date(), self.ep.time(), p[i], l[j], h[k], self.Nw_3D[i, j, k]))

        cursor.executemany(sql, params)

        database.commit()

    def write2npy(self, fname):

        np.save(fname, self.Nw_3D)



    def run(self):

        train_A, train_b, stations = tomography(self.gridp, self.gridl, self.gridh, self.network, self.troposphere, self.mapping_function, self.ep, self.constellation, ())

        print(np.shape(train_A))
        Nw_vec = matrix2vector(self.x0_3D)
        print(np.shape(train_A))
        print(np.shape(train_b))
        print(np.shape(Nw_vec))
        while True:
            Nw_vec, iter_num = mart.mart(train_A, train_b, self.max_iter, Nw_vec, self.tolerance/100)

            train_b_est = np.dot(train_A, Nw_vec)*10**-6


            m, section, r, p, se = stats.linregress(train_b*10**-6, train_b_est)

            regline = lambda x: m*x + section

            diff = train_b_est - regline(train_b*10**-6)

            sigma = float(np.std(diff))

            numOfRay = len(train_b_est)


            indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
            train_A = train_A[indeces,:]
            train_b = train_b[indeces]

            train_b_est = train_b_est[indeces]


            if numOfRay == len(train_b_est):
                break

        self.Nw_3D = vector2matrix(Nw_vec, (self.cellX, self.cellY, self.cellZ))


if __name__ == "__main__":



    #input files
    code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

    source_dir = '../../data/tomography/2021/'
    output_dir = '../../data/tomography/2021/result/'

    #station coordinate file CRD
    station_coords = source_dir+'METEONET.CRD'
    #troposphere files

    gridp_file = 'gridp.csv'
    gridl_file = 'gridl.csv'
    gridh_file = 'gridh.csv'

    gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
    gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
    gridh = np.loadtxt(gridh_file)

    ep = epoch.Epoch(np.array([2021,10,1,6,30,0]), epoch.GPS)

    if ep.dt[3]%6 == 0 and ep.dt[4] == 0 and ep.dt[5] == 0:
        vmf1_grid = [source_dir+'GRD/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep.dt[0],ep.dt[1],ep.dt[2],ep.dt[3]),]
    else:
        ep_min = ep - epoch.Epoch(np.array([0,0,0,ep.dt[3]%6,0,0]))
        ep_max = ep_min + epoch.Epoch(np.array([0,0,0,6,0,0]))
        vmf1_grid = [source_dir+'GRD/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep_min.dt[0],ep_min.dt[1],ep_min.dt[2],ep_min.dt[3]),source_dir+'GRD/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep_max.dt[0],ep_max.dt[1],ep_max.dt[2],ep_max.dt[3])]


    #VMF1 grid file
    #vmf1_grid = [source_dir+'GRD/VMFG_20210811.H00',source_dir+'GRD/VMFG_20210811.H06',source_dir+'GRD/VMFG_20210811.H12',source_dir+'GRD/VMFG_20210811.H18',source_dir+'GRD/VMFG_20210812.H00']
    orography_ell = source_dir+'orography_ell'
    #satellite broadcast files
    brdc_mixed = source_dir+'BRDC/BRDC00WRD_R_20212740000_01D_MN.rnx'
    #epoch of the calculation

    initial_vals_file = source_dir + 'initial.npy'

    x0_3D = np.load(initial_vals_file)

    #x0 = matrix2vector(x0_3D)

    ep = epoch.Epoch(np.array([2021,10,1,3,0,0]), epoch.GPS)

    network = readcrd.ReadCRD(station_coords).network
    brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)

    for sat in brdc.getSatellites():
        network.addSatellite(sat)

    orography = orographyreader.OrographyReader(orography_ell)

    grid = vmf1gridreader.VMF1GridReader(vmf1_grid, orography)
    mapping_function = vmf1.VMF1(grid)

    import dbconfig

    troposphere = readtrp.ReadTRP(database = dbconfig.database, table = 'TRPDELAY', type=readtrp.DB)

    ct = GNSSCT(gridp, gridl, gridh, x0_3D, network, troposphere, mapping_function, ep)

    ct.run()

    ct.writeN2DB(dbconfig.database, '3DREFRACTIVITY')




    #np.save(filename+'.npy',Nw_3D)
    #np.save(source_dir+'initial.npy', x0_3D )
    #np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    #plotRefractivity(filename+'.png', Nw_3D)

    #x0_3D = res[0]
