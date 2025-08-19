import sys
import epoch
import numpy as np
import line
import point
from matrix2vector import matrix2vector
from vector2matrix import vector2matrix
import traceback


## @brief Calculate each rays' length through the tomographic grid and Slant Wet Delay using VIenna Mapping Function 1 for setting up the design matrix a measurements vetor of the equation system
# @file tomography.py
def tomography(proj, gridp, gridl, gridh, network, tropo, mapping_function, ep, constellation=('G','R','E'), ignore_stations=[]):
    """!Calculate each rays' length through the tomographic grid and Slant Wet Delay using VIenna Mapping Function 1 for setting up the design matrix a measurements vetor of the equation system
    @param proj (GetLocal): projections class to get local coordinates from ECEF coordinates
    @param gridp (np.array): tomographic grid (longitude) in radians
    @param gridl (np.array): tomographic grid (latitude) in radians
    @param gridh (np.array): tomographic grid (height) in meters
    @param network (Network): network object that contains all the reference stations and satellite orbits in the reference epoch
    @param tropo (ReadTRP): parsed troposheric delays from Benese TRP file in the reference epoch
    @param mapping_function (VMF1): Vienna Mapping Funtion 1 with the recent VMF1 parameters 
    @param ep (Epoch): refernce epoch
    @param constellations (tuple): list of applied GNSS constellations (G => GPS, R => GLONASS, E => Galileo), diffault: ('G', 'R', 'E') 
    @param ignore_stations (list of station IDs): list of station IDs to be ignored, default: [] 
    @return A (numpy array (n,m)): design matrix (length of rays in each cell)
    @return b (numpy array (n))): measuremnts vector (10^6*SWD values from each station to each satellite)
    @return stations (list (n)): list of stations to the correponding rays
    @retrun satellites (list (n)): list of satellites to the correponding rays
    @return elevation_azimuth (numpy array (n,2)): elevation and azimuth angles to the correponding rays
    """





    matrix = np.empty((0,11))

    #local coordinate system borders
    #lat(rad), lon(rad), height above ellipsoid (meter)
    min = np.array([gridp[0], gridl[0],gridh[0]])
    max = np.array([gridp[-1], gridl[-1],gridh[-1]])


    trafo2local = proj(min, max)

    #grid transformation to local cartesian system
    gridx = trafo2local.x(gridp)
    gridy = trafo2local.y(gridl)
    gridz = trafo2local.z(gridh)

    cellX = len(gridx)-1
    cellY = len(gridy)-1
    cellZ = len(gridz)-1



    cellNum_level = cellX*cellY

    A = np.empty((0,cellX*cellY*cellZ))
    b_w = np.empty((0,))

    stations = []
    satellites = []

    elevation_azimuth = np.empty((0,2))

    
    for sta in network.getStations():

        #skip ignored station
        if sta.id in ignore_stations:
            continue
        
        #station WGS84(lat, lon, h) coordinates
        plh = sta.getPLH()
        #print(plh[0:2,0]*180/np.pi)
        #station transformation to local cartesian system
        loc = trafo2local.getLocalCoords(sta)
        try:
            try:
                zwd = tropo.get_CORR_U(sta.id, ep)
                zhd = tropo.get_MOD_U(sta.id, ep)
                if zwd <= 0:
                    continue
                grad_n = tropo.get_CORR_N(sta.id, ep)
                grad_e = tropo.get_CORR_E(sta.id, ep)
            except IndexError as er:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback)
                continue
            #zwd = grid.getZwd(sta, ep)
            #grad_n = 0
            #grad_e = 0


            #ignore stations outside of the grid
            if not(max[0] >= sta.getPLH()[0,0] >= min[0] and max[1] >= sta.getPLH()[1,0] >=  min[1] and  max[2] >= sta.getPLH()[2,0] >=  min[2]):
                continue

            for sat in network.getSatellites():
                print(sta.id, ep,sat.prn )

                #ignore the not chosen GNSS systems
                if not sat.prn[0] in constellation:
                    continue

                try:
                    #elevation and azimuth angles from ststion to satellite
                    elevAz = sat.getElevAzimuth(sta, ep)
                    #elevation cutoff 10 degrees
                    if elevAz[0]  < 10*np.pi/180:
                        continue
                    if elevAz[0] > 0:

                        
                        #calculate Slant Wed Delay using the Zenit Wet Delay, Vienna Mapping Function and Troposheric Gradients
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

                        minx = gridx[0]# - 0.001
                        maxx = gridx[-1]# +0.001
                        miny = gridy[0]# - 0.001
                        maxy = gridy[-1]# +0.001
                        minz = locxyz[2,0]# - 0.001
                        maxz = gridz[-1]# +0.001




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


                        A_row_3D = np.zeros((cellX, cellY, cellZ))

                        for n in nods[1:,:]:
                            mid = n[3].getXYZ()

                            i = mid[0,0] + mid[1,0]*cellX + mid[2,0]*cellNum_level

                            #A_row[0,i] = n[2]

                            A_row_3D[mid[0,0], mid[1,0], mid[2,0]] = n[2]

                        A_row = matrix2vector(A_row_3D)

                        
                        A = np.append(A, [A_row], axis=0)
                        b_w = np.append(b_w, [swd*10**6])
                        stations.append(sta.id)
                        satellites.append(sat.prn)

                        elevation_azimuth = np.append(elevation_azimuth, [elevAz], axis=0)

                        row = sta.getXYZ().T

                        row = np.append(row, [[elevAz[1]]], axis=1)
                        row = np.append(row, [[elevAz[0]]], axis=1)
                        row = np.append(row, [[swd]], axis=1)

                        coords = sta.getPLH()[:,0]

                        row = np.array([[coords[0]*180/np.pi, coords[1]*180/np.pi, coords[2], np.round(coords[0]*180/np.pi), np.round(coords[1]*180/np.pi), np.round(coords[2]/10)*10, elevAz[1]*180/np.pi, elevAz[0]*180/np.pi, 0, 0, swd]])

                        matrix = np.append(matrix, row, axis=0)


                except epoch.TimeError as er:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback)
                except IndexError as er:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback)
        except KeyError as er:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            pass
        except ValueError as er:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            pass


    #np.savetxt("aaaa.csv", matrix, delimiter=",")
    #np.savetxt("A.csv", A, delimiter=",")
    #np.savetxt("b.csv", b, delimiter=",")











    return (A, b_w, stations, satellites, elevation_azimuth)



    #print(A)
    #print(b)
