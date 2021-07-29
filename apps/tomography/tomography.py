import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import broadcastnavreader
import epoch
import numpy as np
import vmf1gridreader
import vmf1
import getlocal
import line
import point
import mart
from plotrefractivity import plotRefractivity

def tomography(gridp, gridl, gridh, network, tropo, vmf1grid, mapping_function, initial_x, ep, constellation=('G','R','E')):





    matrix = np.empty((0,11))

    #local coordinate system borders
    #lat(rad), lon(rad), height above ellipsoid (meter)
    min = np.array([gridp[0], gridl[0],gridh[0]])
    max = np.array([gridp[-1], gridl[-1],gridh[-1]])


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

            zwd = tropo.get_CORR_U(sta.id, ep)
            if zwd <= 0:
                continue
            grad_n = tropo.get_CORR_N(sta.id, ep)
            grad_e = tropo.get_CORR_E(sta.id, ep)

            #zwd = grid.getZwd(sta, ep)
            #grad_n = 0
            #grad_e = 0

            for sat in network.getSatellites():
                skip_sat = True
                for c in constellation:
                    if sat.prn[0] == c:
                        skip_sat = False
                if skip_sat:
                    continue
                try:
                    elevAz = sat.getElevAzimuth(sta, ep)

                    if elevAz[0]  < 20*np.pi/180:
                        continue


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

                        coords = sta.getPLH()[:,0]

                        row = np.array([[coords[0]*180/np.pi, coords[1]*180/np.pi, coords[2], np.round(coords[0]*180/np.pi), np.round(coords[1]*180/np.pi), np.round(coords[2]/10)*10, elevAz[1]*180/np.pi, elevAz[0]*180/np.pi, 0, 0, swd]])

                        matrix = np.append(matrix, row, axis=0)



                except epoch.TimeError as er:
                    pass
                    #print(er)
        except KeyError as er:
            pass
        except ValueError as er:
            pass

    #np.savetxt("matlab.csv", matrix, delimiter=",")
    np.savetxt("A5.csv", A, delimiter=",")

    print(np.shape(A))
    print(np.shape(b))
    print(np.shape(initial_x))






    res = mart.mart(A, b, 100000, initial_x, 2.7/100)

    #np.savetxt("initial.csv", res['x'], delimiter=",")



    T = np.zeros((cellZ, cellX, cellY))


    for z in range(0,cellZ):
        for y in range(0,cellY):
            for x in range(0,cellX):
                T[z,x,y] = res['x'][z*cellNum_level + y*cellX + x]


    #x = x['x'].reshape((cellZ, cellY, cellX))
    #print(T[0,:,:])
    #print(T[1,:,:])
    #print(T[2,:,:])
    #print(T[3,:,:])
    #print(T[4,:,:])
    #print(T[5,:,:])


    return (T, res['x'])



    #print(A)
    #print(b)
