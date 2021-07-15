import sys
sys.path.append('../src')
sys.path.append('../src/bernese_formats')
import broadcastnavreader
import readcrd
import readtrp
import epoch
import numpy as np
import vmf1gridreader
import vmf1
import getlocal



#input files
source_dir = '../data/tomography/'
#station coordinate file CRD
station_coords = source_dir+'HCONTROL.CRD'
#troposphere files
#Bernese troposphere file TRP
bernese_tropo = source_dir+'CO21173H.TRP'
#VMF1 grid file
vmf1_grid = [source_dir+'VMFG_20201102.H00',source_dir+'VMFG_20201102.H06',source_dir+'VMFG_20201102.H12',source_dir+'VMFG_20201102.H18']
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_S_20211840000_01D_MN.rnx'
#epoch of the calculation
ep = epoch.Epoch(np.array([2021,7,3,6,0,0]))


network = readcrd.ReadCRD(station_coords).network
tropo = readtrp.ReadTRP(bernese_tropo)
grid = vmf1gridreader.VMF1GridReader(vmf1_grid)
mapping_function = vmf1.VMF1(grid)



brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)





for sat in brdc.getSatellites():
    network.addSatellite(sat)


tropo_ep = epoch.Epoch(np.array([2021,6,22,1,0,0]))
grid_ep = epoch.Epoch(np.array([2020,11,2,1,0,0]))

matrix = np.empty((0,5))

#local coordinate system borders
#lat(rad), lon(rad), height above ellipsoid (meter)
min = np.array([40.0*np.pi/180, 1.0*np.pi/180,    0])
max = np.array([53.0*np.pi/180,25.0*np.pi/180,12000])

trafo2local = getlocal.GetLocal(min, max)

for sta in network.getStations():

    plh = sta.getPLH()
    #print(plh[0:2,0]*180/np.pi)

    print(trafo2local.getLocalCoords(sta))
    continue

    try:

        zwd = tropo.get_CORR_U(sta.id, tropo_ep)

        grad_n = tropo.get_CORR_N(sta.id, tropo_ep)
        grad_e = tropo.get_CORR_E(sta.id, tropo_ep)

        for sat in network.getSatellites():
            try:
                elevAz = sat.getElevAzimuth(sta, ep)

                if elevAz[0] > 0:


                    swd = mapping_function.slantDelay_w(zwd, sta, elevAz[1], elevAz[0], grad_n, grad_e, grid_ep)



                    row = np.array([[sta.id, sat.prn, elevAz[1], elevAz[0], swd]])

                    matrix = np.append(matrix, row, axis=0)



            except epoch.TimeError as er:
                print(er)
    except KeyError as er:
        print(er)

print(matrix)
print(np.shape(matrix))
