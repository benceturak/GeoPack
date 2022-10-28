import getopt
import importlib
import sys
sys.path.append("../../src")
from readdb import ReadDB
import epoch
import numpy as np
from scipy.interpolate import griddata
opts, args = getopt.getopt(sys.argv[1:], 'e:', ['gridp=', 'gridl=', 'gridh=', 'epoch=', 'database='])

for o, v in opts:
    if o == '--gridp':
        gridp_file = v
    elif o == '--gridl':
        gridl_file = v
    elif o == '--gridh':
        gridh_file = v
    elif o == '--epoch' or o == '-e':
        dt = v.split('-')
        ep = epoch.Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]), epoch.GPS)
    elif o == '--database' or o == '-d':
        dbconfig = importlib.import_module(v)


db = ReadDB(dbconfig.database)

gridp = np.loadtxt(gridp_file)#*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt(gridl_file)#*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt(gridh_file)

gridp_center = []
gridl_center = []
gridh_center = []
for i in range(0, len(gridp)-1):
    gridp_center.append((gridp[i] + gridp[i+1])/2)

for i in range(0, len(gridl)-1):
    gridl_center.append((gridl[i] + gridl[i+1])/2)

for i in range(0, len(gridh)-1):
    gridh_center.append((gridh[i] + gridh[i+1])/2)

RAOB_stations = []
#layered_profile = []
coords = np.empty((0,2))
temp_at_coords_layers = np.empty((0, len(gridh_center)))

for station in db.getStations("RAOB"):
    RAOB_stations.append(station)

    last_available = db.getLastRAOBSep(station_id=station.id)

    profile = db.getRAOBSTempAtep(station_id=station.id, ep=last_available)

    layered_profile = np.append([gridh_center], [np.interp(gridh_center, profile[:,0], profile[:,1])], axis=0).T

    coords = np.append(coords, station.getPLH()[0:2,:].T, axis=0)
    temp_at_coords_layer = np.empty((len(gridh_center), ))
    for i in range(0, len(gridh_center)):
        temp_at_coords_layer[i] = layered_profile[i,1]


    temp_at_coords_layers = np.append(temp_at_coords_layers, [temp_at_coords_layer], axis=0)

#print(temp_at_coords_layers)

#

temp_model_3d = np.empty((len(gridp_center), len(gridl_center), len(gridh_center)))

##CONSTANTS
k1 = 0.7760
k2 = 0.704
k3 = 0.03739*10**5
Rd = 286.9
Rw = 461.5
###############



interp_gridp, interp_gridl =  np.meshgrid(gridp_center, gridl_center)

#print(interp_gridp)
#print(interp_gridl)
    
for i in range(0, np.shape(temp_at_coords_layers)[1]):
    #print(temp_at_coords_layers[:, i])
    #print(coords)

    

    layer = griddata(coords, temp_at_coords_layers[:,i], (interp_gridp.T, interp_gridl.T), method="nearest")
    temp_model_3d[:,:,i] = layer
    #print(layer)

psat=10**(10.79574*(1-273.16/temp_model_3d)-5.02800*np.log10(temp_model_3d/273.16)+1.50475E-4*(1-(10**(-8.2969*(temp_model_3d/273.16-1))))+4.2873E-4*(10**(4.76955*(1-273.16/((temp_model_3d))))-1)+0.78614);
rows = psat*100/(461.5*temp_model_3d)
Nw, p, l, h = db.getNwAtEp(ep)
WVdensity = Nw/((k2 - k1*Rd/Rw)*Rw + k3*Rw/temp_model_3d)
cursor = dbconfig.database.cursor()
sql = 'INSERT INTO 3DWVDENSITY (DATE, TIME, LAT, LON, ALT, WVDENSITY) VALUES (%s, %s, %s, %s, %s, %s)'
params = []


WVdensity = np.where(rows>=WVdensity, WVdensity, rows)


for i in range(0,np.shape(gridp_center)[0]):
    for j in range(0,np.shape(gridl_center)[0]):
        for k in range(0,np.shape(gridh_center)[0]):
            params.append((ep.date(), ep.time(), gridp_center[i], gridl_center[j], gridh_center[k], WVdensity[i, j, k]))

cursor.executemany(sql, params)

dbconfig.database.commit()