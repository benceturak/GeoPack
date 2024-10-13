import sys
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
import traceback
import gc
import getlocal



class GNSSCT(object):

    def __init__(self, gridp, gridl, gridh, x0_3D_w, x0_3D_h, network, troposphere, mapping_function, ep, constellation=('G', 'R', 'E'), max_iter=3000, tolerance=2.7, output_root="./"):
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

        self.output_root = output_root

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
        p,l,h = self._calcGridCoords()


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
        p,l,h = self._calcGridCoords()


        for i in range(0,np.shape(p)[0]):
            for j in range(0,np.shape(l)[0]):
                for k in range(0,np.shape(h)[0]):
                    params.append((self.ep.date(), self.ep.time(), p[i], l[j], h[k], self.Nw_3D[i, j, k]))#NW !!!!!!!!!!!!!!!!!!!44

        cursor.executemany(sql, params)

        database.commit()

    def writeNw2npy(self, fname):

        np.save(fname, self.Nw_3D)

    def writeNh2npy(self, fname):

        np.save(fname, self.Nh_3D)



    def run(self):

        train_A, train_b_w, stations, satellites, elevAz = tomography(getlocal.GetLocal, self.gridp, self.gridl, self.gridh, self.network, self.troposphere, self.mapping_function, self.ep, self.constellation, ())
        
        stations = np.array(stations)
        satellites = np.array(satellites)
        train_A_w = train_A
        train_A_h = train_A
        #print(np.shape(train_A))
        Nw_vec = matrix2vector(self.x0_3D_w)
        #Nh_vec = matrix2vector(self.x0_3D_h)
        #print(np.shape(train_A))
        #print(np.shape(train_b))

        discarded_stations = np.empty((0,))
        discarded_satellites = np.empty((0,))
        accepted_stations = np.empty((0,))
        accepted_satellites = np.empty((0,))
        #print(satellites[0,1,2,3])

        numOfRaysBefore = np.shape(train_b_w)[0]
        first = True

        i = 0

        #fid = open(self.output_root + "results/rays/all_rays_"+str(self.ep)+".csv", 'a')

        #for i in range(0, len(stations)):
        #    row = str(stations[i]) + "," + str(satellites[i])
        #    print(row , file=fid)


        #fid.close()

        i = 0
        while True:
            print(i)
            Nw_vec, iter_num = mart.mart(train_A_w, train_b_w, self.max_iter, Nw_vec, self.tolerance/100)

            if first:
                pass
            else:
                first = False


            train_b_w_est = np.dot(train_A_w, Nw_vec)*10**-6

            allowedDiffByElev = lambda e: 0.02/np.sin(e)

            allowedDiff = allowedDiffByElev(elevAz[:,0])




            m, section, r, p, se = stats.linregress(train_b_w*10**-6, train_b_w_est)

            regline = lambda x: m*x + section

            diff = train_b_w_est - regline(train_b_w*10**-6)

            sigma = float(np.std(diff))

            numOfRay = len(train_b_w_est)
            #filename = "figures/regression/regression_train_estimated_"+str(self.ep)+"filter"+ str(i)+".png"
            #filename = self.output_root + "results/figures/outliers/Outlier_filter_{1:4d}-{2:02d}-{3:02d}-{4:02d}_(filter_step_{0:d}).tif".format(i, self.ep.dt[0], self.ep.dt[1], self.ep.dt[2], self.ep.dt[3])
            
            diffs = np.abs(train_b_w*10**-6 - train_b_w_est)
            #print(np.shape(elevAz[:,0].T))
            #print(np.shape(diffs))
            forPlot = np.append([elevAz[:,0].T], [diffs], axis=0).T

            #print(forPlot)
            thresholdElev = np.linspace(10,90,100)*np.pi/180#np.array([[10], [90]])
            thresholdSWD = allowedDiffByElev(thresholdElev)

            #print(np.shape(thresholdElev))
            #print(np.shape(thresholdSWD))


            threshold = np.append([thresholdElev*180/np.pi], [thresholdSWD], axis=0).T

            #print(threshold)


            #plotRegression(train_b_w_est, train_b_w*10**-6, filename, "Regression train-estimated (filter: " + str(i) +"):", self.ep, sigma)
            #print(np.shape(np.abs(train_b_w*10**-6, train_b_w_est)))
            


            #indeces = np.where(np.abs(diff) < 3*np.std(diff))[0]
            #print(np.abs(allowedDiff))
            #print(train_b_w*10**-6, train_b_w_est)
            
            indeces = np.where(np.abs(allowedDiff) > diffs)[0]
            discarded_indeces = np.where(np.abs(allowedDiff) <= diffs)[0]

            #print(diffs)
            train_A_w = train_A_w[indeces,:]
            train_b_w = train_b_w[indeces]


            train_b_w_est = train_b_w_est[indeces]
            

            elevAz, discarded_elevAz = elevAz[indeces,:], elevAz[discarded_indeces,:]
            diffs, discarded_diffs = diffs[indeces], diffs[discarded_indeces]

            discarded_forPlot = np.append([discarded_elevAz[:,0].T], [discarded_diffs], axis=0).T

            #plotOutliers(forPlot, discarded_forPlot, threshold, filename)

            discarded_stations = np.append(discarded_stations, stations[discarded_indeces])
            discarded_satellites = np.append(discarded_satellites, satellites[discarded_indeces])


            stations = stations[indeces]
            satellites = satellites[indeces]

            i = i +1
            if numOfRay == len(train_b_w_est):
                break

        #fid = open(self.output_root + 'results/statistic.csv', 'a');
        numOfRaysAfter = np.shape(train_b_w)[0]

        #print(str(self.ep)+","+str(numOfRaysBefore)+","+str(numOfRaysAfter), file=fid)

        #fid.close()



        #fid = open(self.output_root + "results/rays/discarded_rays_"+str(self.ep)+".csv", 'a')

        #for i in range(0, len(discarded_stations)):
        #    row = str(discarded_stations[i]) + "," + str(discarded_satellites[i])
        #    print(row , file=fid)


        #fid.close()
        



        self.Nw_3D = vector2matrix(Nw_vec, (self.cellX, self.cellY, self.cellZ))
        filename = self.output_root + "results/figures/refractivity/refractivity_{0:4d}-{1:02d}-{2:02d}-{3:02d}.tif".format(ep.dt[0], ep.dt[1], ep.dt[2], ep.dt[3])
        #plotRefractivity(filename, self.Nw_3D, self.ep)

        gc.collect()



if __name__ == "__main__":
    import getopt
    import importlib
    opts, args = getopt.getopt(sys.argv[1:], 's:S:e:i:v:t:', ['satellites=', 'stations=', 'gridp=', 'gridl=', 'gridh=', 'vmf1loc=', 'initial_w=', 'epoch=', 'tropofile='])
    print(opts)

    for o, v in opts:
        if o == '--satellites' or o == '-s':
            sats = v
            sat_files = v.split("|")
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
        elif o == '--tropofile' or o == '-t':
            tropofile = v
        elif o == '--epoch' or o == '-e':
            dt = v.split('-')

            ep = epoch.Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]), epoch.GPS)

    

    #input files
    code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

    gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
    gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
    gridh = np.loadtxt(gridh_file)

    #ep = epoch.Epoch(np.array([2021,10,1,6,30,0]), epoch.GPS)

    if ep.dt[3]%6 == 0 and ep.dt[4] == 0 and ep.dt[5] == 0:
        vmf1_grid = ['{:s}{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(vmf1grid_loc, ep.dt[0],ep.dt[0],ep.dt[1],ep.dt[2],ep.dt[3]),]
    else:
        ep_min = ep - epoch.Epoch(np.array([0,0,0,ep.dt[3]%6,0,0]))
        ep_max = ep_min + epoch.Epoch(np.array([0,0,0,6,0,0]))
        vmf1_grid = ['{:s}{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(vmf1grid_loc, ep_min.dt[0],ep_min.dt[0],ep_min.dt[1],ep_min.dt[2],ep_min.dt[3]),'{:s}{:4d}/VMFG_{:4d}{:02d}{:02d}.H{:02d}'.format(vmf1grid_loc, ep_max.dt[0],ep_max.dt[0],ep_max.dt[1],ep_max.dt[2],ep_max.dt[3])]


    #VMF1 grid file
    #vmf1_grid = [source_dir+'GRD/VMFG_20210811.H00',source_dir+'GRD/VMFG_20210811.H06',source_dir+'GRD/VMFG_20210811.H12',source_dir+'GRD/VMFG_20210811.H18',source_dir+'GRD/VMFG_20210812.H00']
    orography_ell = vmf1grid_loc+'orography_ell'
    #satellite broadcast files
    #brdc_mixed = source_dir+'BRDC/BRDC00WRD_R_20212740000_01D_MN.rnx'
    #epoch of the calculation

    #initial_vals_file = source_dir + 'initial.npy'

    #x0_3D_w = np.load(initial_w_vals_file)
    #x0_3D_h = np.load(initial_h_vals_file)

    '''
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
    '''
    x0_3D_w_profile = np.loadtxt(initial_w_vals_file, delimiter=",", usecols=(1,6), skiprows=1)
    
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

    for sat in sat_files:
        print(sat)
        try:
            brdc = sp3reader.SP3Reader(sat)
            break
        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            continue

    #print(brdc.getSatellite('G01'))

    
    print(ep)
    for sat in brdc.getSatellites():
        network.addSatellite(sat)

    


    orography = orographyreader.OrographyReader(orography_ell)

    grid = vmf1gridreader.VMF1GridReader(vmf1_grid, orography)
    mapping_function = vmf1.VMF1(grid)

    #import dbconfig
    
    troposphere = readtrp.ReadTRP(fileName=tropofile, type=readtrp.TXT)

    ct = GNSSCT(gridp, gridl, gridh, x0_3D_w, np.array([]), network, troposphere, mapping_function, ep,output_root="")

    ct.run()
    output = "results/refractivity/refractivity_{0:4d}-{1:02d}-{2:02d}-{3:02d}.npy".format(ep.dt[0], ep.dt[1], ep.dt[2], ep.dt[3])
            
    ct.writeNw2npy(output)
    #ct.writeNh2npy(initial_h_vals_file)




    #np.save(filename+'.npy',Nw_3D)
    #np.save(source_dir+'initial.npy', x0_3D )
    #np.save(source_dir+'initial_'+c+'.npy', x0_3D )



    #plotRefractivity(filename+'.png', Nw_3D)

    #x0_3D = res[0]
