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
import line
import point
import mart


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
tropo_ep = epoch.Epoch(np.array([2021,6,22,1,0,0]))#just for the test!!!!!!!!
grid_ep = epoch.Epoch(np.array([2020,11,2,1,0,0]))#just for the test!!!!!!!!


network = readcrd.ReadCRD(station_coords).network
tropo = readtrp.ReadTRP(bernese_tropo)
grid = vmf1gridreader.VMF1GridReader(vmf1_grid)
mapping_function = vmf1.VMF1(grid)



brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)





for sat in brdc.getSatellites():
    network.addSatellite(sat)




matrix = np.empty((0,5))

#local coordinate system borders
#lat(rad), lon(rad), height above ellipsoid (meter)
min = np.array([40.0*np.pi/180, 1.0*np.pi/180,    0])
max = np.array([53.0*np.pi/180,25.0*np.pi/180,12000])

gridp = np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.arange(min[1], max[1], 0.6*np.pi/180)
gridh = np.array([0,1000,2000,3000,5500,8000,12000])

trafo2local = getlocal.GetLocal(min, max)

gridx = trafo2local.x(gridp)
gridy = trafo2local.y(gridl)
gridz = trafo2local.z(gridh)

cellX = len(gridx)-1
cellY = len(gridy)-1
cellZ = len(gridz)-1

cellNum_level = cellX*cellY
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(gridx[0], gridx[-1])
ax.set_ylim(gridy[0], gridy[-1])
#ax.set_zlim(gridz[0], gridz[-1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


A = np.empty((0,cellX*cellY*cellZ))
b = np.empty((0,1))


for sta in network.getStations():

    plh = sta.getPLH()
    #print(plh[0:2,0]*180/np.pi)

    loc = trafo2local.getLocalCoords(sta)


    try:

        #zwd = tropo.get_CORR_U(sta.id, tropo_ep)


        #grad_n = tropo.get_CORR_N(sta.id, tropo_ep)
        #grad_e = tropo.get_CORR_E(sta.id, tropo_ep)

        zwd = grid.getA_w(sta, grid_ep)
        grad_n = 0
        grad_e = 0

        for sat in network.getSatellites():
            try:
                elevAz = sat.getElevAzimuth(sta, ep)

                if elevAz[0] > 0:


                    swd = mapping_function.slantDelay_w(zwd, sta, elevAz[1], elevAz[0], grid_ep, grad_n, grad_e)

                    ray = line.Line(loc, elevAz[1], elevAz[0])
                    #print(sta.getPLH()[0:2,0]*180/np.pi)
                    #print(loc)

                    locxyz = loc.getXYZ()

                    nods = np.array([loc])
                    x = np.empty((0,))
                    y = np.empty((0,))
                    z = np.empty((0,))
                    for a in ray.getPointAtT(ray.getTwhereZ([0])):
                        pass#print(a)

                    for sec in ray.getPointAtT(ray.getTwhereX(gridx)):
                        if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and gridz[-1] >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            nods = np.append(nods, sec)

                    for sec in ray.getPointAtT(ray.getTwhereY(gridy)):
                        if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and gridz[-1] >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            nods = np.append(nods, sec)

                    for sec in ray.getPointAtT(ray.getTwhereZ(gridz)):
                        if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and gridz[-1] >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            nods = np.append(nods, sec)



                    #print(nods)

                    if nods[-1].getXYZ()[2,0] == 12000.0:


                        d = np.empty((0,))
                        dsum = np.empty((0,))
                        first = True


                        for n in nods:


                            if not first:
                                d = np.append(d, nods[0].dist(n) - dsum[-1])
                            else:
                                d = np.append(d, [0])
                                first = False
                            dsum = np.append(dsum, nods[0].dist(n))


                            x = np.append(x, n.getXYZ()[1,0])
                            y = np.append(y, n.getXYZ()[0,0])
                            z = np.append(z, n.getXYZ()[2,0])

                        nods = np.append([nods], [dsum], axis=0)
                        nods = np.append(nods, [d], axis=0).T
                        nods = nods[np.argsort(nods[:, 1])]

                        first = True
                        midPoints = np.empty((0,))

                        for n in nods:
                            now = n[0].getXYZ()
                            if not first:
                                midp = (last + now)/2

                                for i in range(0,cellX):
                                    if gridx[i] < midp[1,0] < gridx[i+1]:
                                        cx = i

                                for i in range(0,cellY):
                                    if gridy[i] < midp[0,0] < gridy[i+1]:
                                        cy = i
                                for i in range(0,cellZ):
                                    if gridz[i] < midp[2,0] < gridz[i+1]:
                                        cz = i

                                midPoints = np.append(midPoints, point.Point(coord=np.array([cx,cy,cz])))

                            else:
                                midPoints = np.append(midPoints, point.Point(coord=np.array([-1,-1,-1])))
                                first = False
                            last = now

                        nods = np.append(nods.T, [midPoints], axis=0).T



                        A_row = np.zeros((1,cellX*cellY*cellZ))

                        for n in nods[1:,:]:
                            mid = n[3].getXYZ()

                            i = mid[1,0] + mid[0,0]*cellY + mid[2,0]*cellNum_level

                            A_row[0,i] = n[2]



                        A = np.append(A, A_row, axis=0)
                        b = np.append(b, [[swd*10**6]], axis=0)


                        x = np.append(x[0], x[-1])
                        y = np.append(y[0], y[-1])
                        z = np.append(z[0], z[-1])

                        ax.scatter(locxyz[1,0], locxyz[0,0], locxyz[2,0])
                        ax.plot3D(x, y, z)




                        row = np.array([[sta.id, sat.prn, elevAz[1], elevAz[0], swd]])

                        matrix = np.append(matrix, row, axis=0)



            except epoch.TimeError as er:
                print(er)
    except KeyError as er:
        print(er)
plt.show()

#print(matrix)
#print(np.shape(matrix))
mart.mart(A, b, 100, A[0,:], 1)
#print(A)
#print(b)

print(np.shape(A))
#print(np.shape(b))
