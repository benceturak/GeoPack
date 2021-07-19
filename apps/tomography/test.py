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
import station
from ellipsoid import WGS84

source_dir = '../../data/tomography/'


data = np.genfromtxt('adatok.csv', delimiter=',')

min = np.array([45.5*np.pi/180, 15.5*np.pi/180,    0])
max = np.array([49.0*np.pi/180, 23.0*np.pi/180,12000])

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

trafo2local = getlocal.GetLocal(min, max)

A = np.empty((0,cellX*cellY*cellZ))
b = np.empty((0,))


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(gridx[0], gridx[-1])
ax.set_ylim(gridy[0], gridy[-1])
ax.set_zlim(gridz[0], gridz[-1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

print(np.shape(data))


for row in data:
    sta = station.Station(coord=np.array([row[0],row[1],row[2]]), type=1, system=WGS84())


    loc = trafo2local.getLocalCoords(sta)

    alpha = row[3]
    elev = row[4]
    swd = row[5]




    ray = line.Line(loc, alpha, elev)

    locxyz = loc.getXYZ()

    nods = np.array([loc])
    x = np.empty((0,))
    y = np.empty((0,))
    z = np.empty((0,))




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


        x = np.append(x, nods[i].getXYZ()[0,0])
        y = np.append(y, nods[i].getXYZ()[1,0])
        z = np.append(z, nods[i].getXYZ()[2,0])

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


    #x = np.append(x[0], x[-1])
    #y = np.append(y[0], y[-1])
    #z = np.append(z[0], z[-1])

    ax.scatter(locxyz[0,0], locxyz[1,0], locxyz[2,0])
    ax.plot3D(x, y, z)




    #row = np.array([[sta.id, sat.prn, elevAz[1], elevAz[0], swd]])

    #matrix = np.append(matrix, row, axis=0)





    #else:


        #print(elev*180/np.pi)
        #print(nods)

        #xx = yy = zz = np.empty((0,))
        #for n in nods:
            #xxyyzz = n[0].getXYZ()[:,0]

            #xx = np.append(xx, xxyyzz[1])
            #yy = np.append(yy, xxyyzz[0])
            #zz = np.append(zz, xxyyzz[2])
        #ax.scatter(locxyz[1,0], locxyz[0,0], locxyz[2,0])
        #ax.plot3D(xx, yy, zz)
        #print('--------------------------------------------')



plt.show()





print(np.shape(A))
print(np.shape(b))


ccc = int(np.shape(A)[1]/6)

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

R = np.random.permutation(450)
#np.savetxt("A.csv", A, delimiter=",")
#np.savetxt("b.csv", b, delimiter=",")
#A = A[R,:]
#b = b[R]


print(np.shape(A))
print(np.shape(b))

mart.mart(A, b, 300, x0, 2.7/100)
