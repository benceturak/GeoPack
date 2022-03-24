import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import epoch
import gnssct
import numpy as np
import readcrd
import sp3reader
import orographyreader
import vmf1gridreader
import vmf1
import readtrp
import dbconfig
from gnssct_postprocess import GNSSCT
#input files
code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

#source_dir = '../../data/tomography/2021/'
#output_dir = '../../data/tomography/2021/result/'

#station coordinate file CRD
#station_coords = source_dir+'METEONET.CRD'
#troposphere files
grid_dir = "/home/bence/data/GeoPack/apps/tomography/"
gridp_file = grid_dir + 'gridp.csv'
gridl_file = grid_dir + 'gridl.csv'
gridh_file = grid_dir + 'gridh.csv'
gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt(gridh_file)

satellite_orbit_dir = "/home/bence/nrt/code_orbits/postprocessing/"

vmf1grid_loc = "/home/bence/nrt/vmf1/"

initial_w_vals_file = "/home/bence/nrt/tomography/initial_w.npy"

station_coords = "/home/bence/nrt/METEONET.CRD"
vmf1grid_loc = "/home/bence/nrt/vmf1/"

ep_start = epoch.Epoch(np.array([2022,3,1,0,0,0]))
ep_end = epoch.Epoch(np.array([2022,3,14,23,0,0]))

ep = ep_start

eps = []

while ep <= ep_end:


    eps.append(ep)

    ep = ep + epoch.Epoch(np.array([0,0,0,1,0,0]))

for ep in eps:
    print(ep)
    orbit_hour = "{:02d}".format(int(ep.dt[3]/6)*6)
    print()

    brdc_mixed = satellite_orbit_dir + "CDU" + str(ep.GPSweek) + str(ep.DOW) + "_" + str(orbit_hour)+ ".EPH"
    print(brdc_mixed)



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

    x0_3D_w = np.load(initial_w_vals_file)
    x0_3D_h = np.load(initial_w_vals_file)

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

    ct.writeNW2DB(dbconfig.database, '3DREFRACTIVITY_H')
    #ct.writeNH2DB(dbconfig.database, '3DREFRACTIVITY_H')

    ct.writeNw2npy(initial_w_vals_file)
    #ct.writeNh2npy(initial_h_vals_file)




#np.save(filename+'.npy',Nw_3D)
#np.save(source_dir+'initial.npy', x0_3D )
#np.save(source_dir+'initial_'+c+'.npy', x0_3D )



#plotRefractivity(filename+'.png', Nw_3D)

#x0_3D = res[0]
