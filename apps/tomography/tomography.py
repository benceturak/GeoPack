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
import getlocal
import line
import point
import mart


#input files
source_dir = '../../data/tomography/'
#station coordinate file CRD
station_coords = source_dir+'HCONTROL.CRD'
#troposphere files
#Bernese troposphere file TRP
bernese_tropo = source_dir+'CO21173H.TRP'
#VMF1 grid file
vmf1_grid = [source_dir+'VMFG_20201102.H00',source_dir+'VMFG_20201102.H06',source_dir+'VMFG_20201102.H12',source_dir+'VMFG_20201102.H18']
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_S_20203070000_01D_MN.rnx'
#epoch of the calculation
ep = epoch.Epoch(np.array([2020,11,2,0,0,0]))
#tropo_ep = epoch.Epoch(np.array([2021,6,22,1,0,0]))#just for the test!!!!!!!!
#grid_ep = epoch.Epoch(np.array([2020,11,2,1,0,0]))#just for the test!!!!!!!!


network = readcrd.ReadCRD(station_coords).network
tropo = readtrp.ReadTRP(bernese_tropo)
grid = vmf1gridreader.VMF1GridReader(vmf1_grid)
mapping_function = vmf1.VMF1(grid)



brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)





for sat in brdc.getSatellites():
    network.addSatellite(sat)




matrix = np.empty((0,6))

#local coordinate system borders
#lat(rad), lon(rad), height above ellipsoid (meter)
min = np.array([45.5*np.pi/180, 15.5*np.pi/180,    0])
max = np.array([49.0*np.pi/180, 23.0*np.pi/180,12000])

gridp = np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.array([0,1000,2000,3000,5500,8000,12000])

gridp = np.array([45.5,46.2,46.9,47.6,48.3,49.0])*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.array([15.5,17.0,18.5,20.0,21.5,23.0])*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.array([0,1000,2000,3000,5500,8000,12000])





trafo2local = getlocal.GetLocal(min, max)

gridx = trafo2local.x(gridp)
gridy = trafo2local.y(gridl)
gridz = trafo2local.z(gridh)

cellX = len(gridx)-1
cellY = len(gridy)-1
cellZ = len(gridz)-1

cellNum_level = cellX*cellY


A = np.empty((0,cellX*cellY*cellZ))
b = np.empty((0,))


for sta in network.getStations():

    plh = sta.getPLH()
    #print(plh[0:2,0]*180/np.pi)

    loc = trafo2local.getLocalCoords(sta)


    try:

        #zwd = tropo.get_CORR_U(sta.id, tropo_ep)


        #grad_n = tropo.get_CORR_N(sta.id, tropo_ep)
        #grad_e = tropo.get_CORR_E(sta.id, tropo_ep)

        zwd = grid.getA_w(sta, ep)
        grad_n = 0
        grad_e = 0

        for sat in network.getSatellites():
            #print(sta.id + "|" + sat.prn)
            try:
                elevAz = sat.getElevAzimuth(sta, ep)


                if elevAz[0] > 0:


                    swd = mapping_function.slantDelay_w(zwd, sta, elevAz[1], elevAz[0], ep, grad_n, grad_e)

                    ray = line.Line(loc, elevAz[1], elevAz[0])
                    #print(sta.getPLH()[0:2,0]*180/np.pi)
                    #print(loc)

                    locxyz = loc.getXYZ()

                    nods = np.array([loc])


                    for sec in ray.getPointAtT(ray.getTwhereX(gridx)):
                        if np.all(sec.getXYZ() != locxyz):
                            nods = np.append(nods, sec)
                        #if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and (gridz[-1]+1) >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            #nods = np.append(nods, sec)

                    for sec in ray.getPointAtT(ray.getTwhereY(gridy)):
                        if np.all(sec.getXYZ() != locxyz):
                            nods = np.append(nods, sec)
                        #if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and (gridz[-1]+1) >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            #nods = np.append(nods, sec)
                    for sec in ray.getPointAtT(ray.getTwhereZ(gridz)):
                        if np.all(sec.getXYZ() != locxyz):
                            nods = np.append(nods, sec)
                        #if gridx[-1] >= sec.getXYZ()[1,0] >= gridx[0] and gridy[-1] >= sec.getXYZ()[0,0] >= gridy[0] and (gridz[-1]+1) >= sec.getXYZ()[2,0] >= locxyz[2,0]:
                            #nods = np.append(nods, sec



                    nods_temp = np.empty((0,))

                    minx = gridx[0] - 1
                    maxx = gridx[-1] +1
                    miny = gridy[0] - 1
                    maxy = gridy[-1] +1
                    minz = locxyz[2,0] - 1
                    maxz = gridz[-1] +1




                    for n in nods:
                        if  maxx >= n.getXYZ()[0,0] >= minx and maxy >= n.getXYZ()[1,0] >= miny and maxz >= n.getXYZ()[2,0] >= minz:
                            nods_temp = np.append(nods_temp, n)

                    nods = nods_temp





                    d = np.array([0])
                    dsum = np.array([0])

                    for i in range(1,len(nods)):
                        dsum = np.append(dsum, nods[0].dist(nods[i]))


                    if np.shape(nods)[0] == 0:
                        continue
                    nods = np.append([nods], [dsum], axis=0).T


                    nods = nods[np.argsort(nods[:, 1])]


                    #ray_check.ray_check(locxyz[:,0], [alpha, elev], gridx, gridy, gridz):
                    if nods[-1,0].getXYZ()[2,0] < 11999.0:
                        continue
                    #else:
                    #    print(nods[-1,0].getXYZ()[2,0])

                    for i in range(1,np.shape(nods)[0]):
                        d = np.append(d, nods[i,0].dist(nods[i-1,0]))

                    d = np.array([d]).T
                    nods = np.append(nods, d, axis=1)





                    first = True
                    midPoints = np.empty((0,))

                    for n in nods:
                        now = n[0].getXYZ()
                        if not first:
                            midp = (last + now)/2

                            for i in range(0,cellX):
                                if gridx[i] < midp[0,0] < gridx[i+1]:
                                    cx = i

                            for i in range(0,cellY):
                                if gridy[i] < midp[1,0] < gridy[i+1]:
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

                        i = mid[0,0] + mid[1,0]*cellX + mid[2,0]*cellNum_level

                        A_row[0,i] = n[2]



                    A = np.append(A, A_row, axis=0)
                    b = np.append(b, [swd*10**6])





                    row = sta.getXYZ().T

                    row = np.append(row, [[elevAz[1]]], axis=1)
                    row = np.append(row, [[elevAz[0]]], axis=1)
                    row = np.append(row, [[swd]], axis=1)

                    #row = np.array([[sta.id, sat.prn, elevAz[1], elevAz[0], swd]])

                    matrix = np.append(matrix, row, axis=0)



            except epoch.TimeError as er:
                pass
                #print(er)
    except KeyError as er:
        pass
        #print(er)
print(np.shape(A))
print(np.shape(b))
#print(matrix)
#print(np.shape(matrix))

ccc = int(np.shape(A)[1]/6)
np.savetxt("adatok.csv", matrix, delimiter=",")
x01 = np.ones((ccc,))*46.5
x02 = np.ones((ccc,))*43.2
x03 = np.ones((ccc,))*34.8
x04 = np.ones((ccc,))*23.3
x05 = np.ones((ccc,))* 7.4
x06 = np.ones((ccc,))* 0.6

x0 = np.append(x01, x02)
x0 = np.append(x0, x03)
x0 = np.append(x0, x04)
x0 = np.append(x0, x05)
x0 = np.append(x0, x06)

x0 = x0.T
i = 0
for c in A.T:
    if np.all(c == 0):
        print(i)
    i = i+1




mart.mart(A, b, 1000, x0, 2.7/100)


#print(A)
#print(b)
