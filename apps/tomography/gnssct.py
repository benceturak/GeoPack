import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import broadcastnavreader
import sp3reader
import readcrd
import readtrp
import orographyreader
import epoch
import numpy as np
from scipy import stats
import vmf1gridreader
import vmf1
import mart
from vector2matrix import vector2matrix
from matrix2vector import matrix2vector
from tomography import tomography
import station



class GNSSCT(object):

    def __init__(self, gridp, gridl, gridh, x0_3D_w, x0_3D_h, network, troposphere, mapping_function, ep, constellation=('G', 'R', 'E'), max_iter=3000, tolerance=2.7):
        self.gridp = gridp
        self.gridl = gridl
        self.gridh = gridh

        self.cellX = len(self.gridp)-1
        self.cellY = len(self.gridl)-1
        self.cellZ = len(self.gridh)-1


        self.x0_3D_w = x0_3D_w#np.load(initial_vals_file)
        self.x0_3D_h = x0_3D_h

        self.network = network

        self.troposphere = troposphere

        self.ep = ep

        self.mapping_function = mapping_function

        self.constellation = constellation

        self.max_iter = max_iter
        self.tolerance = tolerance

        self.Nw_3D = None
        self.Nh_3D = None

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




    def writeNW2DB(self, database, table):
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

    def writeNH2DB(self, database, table):
        cursor = database.cursor()
        sql = 'INSERT INTO ' + table + ' (DATE, TIME, LAT, LON, ALT, NH) VALUES (%s, %s, %s, %s, %s, %s)'
        params = []
        p,l,h = ct._calcGridCoords()


        for i in range(0,np.shape(p)[0]):
            for j in range(0,np.shape(l)[0]):
                for k in range(0,np.shape(h)[0]):
                    params.append((self.ep.date(), self.ep.time(), p[i], l[j], h[k], self.Nh_3D[i, j, k]))

        cursor.executemany(sql, params)

        database.commit()

    def writeNw2npy(self, fname):

        np.save(fname, self.Nw_3D)

    def writeNh2npy(self, fname):

        np.save(fname, self.Nh_3D)



    def run(self):

        train_A, train_b_w, train_b_h, stations, satellites = tomography(self.gridp, self.gridl, self.gridh, self.network, self.troposphere, self.mapping_function, self.ep, self.constellation, ())

        train_A_w = train_A
        train_A_h = train_A
        print(np.shape(train_A))
        Nw_vec = matrix2vector(self.x0_3D_w)
        Nh_vec = matrix2vector(self.x0_3D_h)
        print(np.shape(train_A))
        #print(np.shape(train_b))
        print(np.shape(Nw_vec))
        print(np.shape(Nh_vec))
        while True:
            Nw_vec, iter_num = mart.mart(train_A_w, train_b_w, self.max_iter, Nw_vec, self.tolerance/100)

            train_b_w_est = np.dot(train_A_w, Nw_vec)*10**-6


            m, section, r, p, se = stats.linregress(train_b_w*10**-6, train_b_w_est)

            regline = lambda x: m*x + section

            diff = train_b_w_est - regline(train_b_w*10**-6)

            sigma = float(np.std(diff))

            numOfRay = len(train_b_w_est)


            indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
            train_A_w = train_A_w[indeces,:]
            train_b_w = train_b_w[indeces]

            train_b_w_est = train_b_w_est[indeces]


            if numOfRay == len(train_b_w_est):
                break

        self.Nw_3D = vector2matrix(Nw_vec, (self.cellX, self.cellY, self.cellZ))

        """while True:
            Nh_vec, iter_num = mart.mart(train_A_h, train_b_h, self.max_iter, Nh_vec, self.tolerance/100)

            train_b_h_est = np.dot(train_A_h, Nh_vec)*10**-6
            print(np.shape(train_b_h_est*10**-6))
            print(np.shape(train_b_h))


            m, section, r, p, se = stats.linregress(train_b_h*10**-6, train_b_h_est)

            regline = lambda x: m*x + section

            diff = train_b_h_est - regline(train_b_h*10**-6)

            sigma = float(np.std(diff))

            numOfRay = len(train_b_h_est)


            indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
            train_A_h = train_A_h[indeces,:]
            train_b_h = train_b_h[indeces]

            train_b_h_est = train_b_h_est[indeces]


            if numOfRay == len(train_b_h_est):
                break

        self.Nh_3D = vector2matrix(Nh_vec, (self.cellX, self.cellY, self.cellZ))"""


if __name__ == "__main__":
    import getopt
    import importlib
    opts, args = getopt.getopt(sys.argv[1:], 's:S:e:i:v:d:', ['satellites=', 'stations=', 'gridp=', 'gridl=', 'gridh=', 'vmf1loc=', 'initial_w=', 'initial_h=', 'epoch=', 'database='])
    print(opts)

    for o, v in opts:
        if o == '--satellites' or o == '-s':
            sats = v
            brdc_mixed = v
        elif o == '--stations' or o == '-S':
            station_coords = v
        elif o == '--gridp':
            gridp_file = v
        elif o == '--gridl':
            gridl_file = v
        elif o == '--gridh':
            gridh_file = v
        elif o == '--vmf1loc' or o == '-v':
            vmf1grid_loc = v
        elif o == '--initial_w' or o == '-i':
            initial_w_vals_file = v
        elif o == '--initial_h':
            initial_h_vals_file = v
        elif o == '--epoch' or o == '-e':
            dt = v.split('-')

            ep = epoch.Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]), epoch.GPS)
        elif o == '--database' or o == '-d':
            print('aaa')
            dbconfig = importlib.import_module(v)







    #input files
    code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

    #source_dir = '../../data/tomography/2021/'
    #output_dir = '../../data/tomography/2021/result/'

    #station coordinate file CRD
    #station_coords = source_dir+'METEONET.CRD'
    #troposphere files

    #gridp_file = 'gridp.csv'
    #gridl_file = 'gridl.csv'
    #gridh_file = 'gridh.csv'

    gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
    gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
    gridh = np.loadtxt(gridh_file)

    #ep = epoch.Epoch(np.array([2021,10,1,6,30,0]), epoch.GPS)

    if ep.dt[3]%6 == 0 and ep.dt[4] == 0 and ep.dt[5] == 0:
        vmf1_grid = [vmf1grid_loc+'{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep.dt[0],ep.dt[0],ep.dt[1],ep.dt[2],ep.dt[3]),]
    else:
        ep_min = ep - epoch.Epoch(np.array([0,0,0,ep.dt[3]%6,0,0]))
        ep_max = ep_min + epoch.Epoch(np.array([0,0,0,6,0,0]))
        vmf1_grid = [vmf1grid_loc+'{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep_min.dt[0],ep_min.dt[0],ep_min.dt[1],ep_min.dt[2],ep_min.dt[3]),vmf1grid_loc+'{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(ep_max.dt[0],ep_max.dt[0],ep_max.dt[1],ep_max.dt[2],ep_max.dt[3])]


    #VMF1 grid file
    #vmf1_grid = [source_dir+'GRD/VMFG_20210811.H00',source_dir+'GRD/VMFG_20210811.H06',source_dir+'GRD/VMFG_20210811.H12',source_dir+'GRD/VMFG_20210811.H18',source_dir+'GRD/VMFG_20210812.H00']
    orography_ell = vmf1grid_loc+'orography_ell'
    #satellite broadcast files
    #brdc_mixed = source_dir+'BRDC/BRDC00WRD_R_20212740000_01D_MN.rnx'
    #epoch of the calculation

    #initial_vals_file = source_dir + 'initial.npy'

    #x0_3D_w = np.load(initial_w_vals_file)
    x0_3D_h = np.load(initial_h_vals_file)
    epForRequest = ep
    while(1):
        epForRequest = epForRequest - epoch.Epoch(np.array([0,0,0,1,0,0]))
        sql = "SELECT HEIGHT, N_WET FROM RAOBSREFR WHERE DATE='"+epForRequest.date()+"' AND TIME='"+epForRequest.time()+"' AND WMOID="+ str(12843) +" ORDER BY HEIGHT ASC"
        dbcursor = dbconfig.database.cursor()
        dbcursor.execute(sql)

        x0_3D_w_profile = np.empty((0,2))
        for s in dbcursor.fetchall():

            x0_3D_w_profile = np.append(x0_3D_w_profile, [[s[0], s[1]]], axis=0)
        if(np.shape(x0_3D_w_profile)[0] > 0):
            break

    x0_3D_w = np.empty((len(gridp)-1,len(gridl)-1,len(gridh)-1))

    nanret = False
    for i in range(0,len(gridh)-1):
        layer = x0_3D_w_profile[np.all((x0_3D_w_profile[:,0]>=gridh[i],x0_3D_w_profile[:,0]<=gridh[i+1]),axis=0)]
        N = np.mean(layer[:,1])
        if not np.isnan(N):
            x0_3D_w[:,:,i] = N
            if nanret:
                x0_3D_w[:,:,i-1] = N
                nanret = False

        else:
            if i > 0:
                x0_3D_w[:,:,i] = x0_3D_w[:,:,i-1]
            else:
                nanret = True

    #x0 = matrix2vector(x0_3D)

    #ep = epoch.Epoch(np.array([2021,10,1,3,0,0]), epoch.GPS)

    network = readcrd.ReadCRD(station_coords).network
    #brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)
    brdc = sp3reader.SP3Reader(brdc_mixed)

    #print(brdc.getSatellite('G01'))


    print(ep)
    for sat in brdc.getSatellites():
        network.addSatellite(sat)


    orography = orographyreader.OrographyReader(orography_ell)

    grid = vmf1gridreader.VMF1GridReader(vmf1_grid, orography)
    mapping_function = vmf1.VMF1(grid)

    #import dbconfig

    troposphere = readtrp.ReadTRP(database = dbconfig.database, table = 'TRPDELAY', type=readtrp.DB)

    ct = GNSSCT(gridp, gridl, gridh, x0_3D_w, x0_3D_h, network, troposphere, mapping_function, ep)

    ct.run()

    ct.writeNW2DB(dbconfig.database, '3DREFRACTIVITY_W')
    #ct.writeNH2DB(dbconfig.database, '3DREFRACTIVITY_H')

    ct.writeNw2npy(initial_w_vals_file)
    #ct.writeNh2npy(initial_h_vals_file)




    #np.save(filename+'.npy',Nw_3D)
    #np.save(source_dir+'initial.npy', x0_3D )
    #np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    #plotRefractivity(filename+'.png', Nw_3D)

    #x0_3D = res[0]
