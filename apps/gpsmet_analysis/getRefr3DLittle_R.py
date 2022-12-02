#!/usr/bin/python3

try:
    import sys
    import traceback

    sys.path.append("/home/bence/data/GeoPack/src")
    from readdb import ReadDB
    from little_rwriter import Little_RWriter
    from little_rwriter import Little_RStation
    from epoch import Epoch
    import dbconfig
    import numpy as np
    import getopt
    import importlib
    from scipy.interpolate import griddata
    opts, args = getopt.getopt(sys.argv[1:], 'e:o:h:', ['epoch=', 'gridp=', 'gridl=', 'gridh=','output=', 'help'])
    stations = None



    for o, v in opts:
        if o == '--epoch' or o == '-e':
            dt = v.split('-')
            ep = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
        elif o == '--gridp':
            gridp_file = v
        elif o == '--gridl':
            gridl_file = v
        elif o == '--gridh':
            gridh_file = v
        elif o == '--output' or o == '-o':
            filename = v

        elif  o == '--help' or o == '-h':
            print("Usage:")


    database = ReadDB(database=dbconfig.database)

   
    

    if True:
        
        Nw_model, gridp_center, gridl_center, gridh_center = database.getNwAtEp(ep)


        #fr = Epoch(np.array([2021,11,1,2,0,0]))
        #to = Epoch(np.array([2021,11,1,3,0,0]))
        writer = Little_RWriter(filename)
        RAOB_stations = []
        coords = np.empty((0,2))
        temp_at_coords_layers = np.empty((0, len(gridh_center)))
        press_at_coords_layers = np.empty((0, len(gridh_center)))
        Nh_at_coords_layers = np.empty((0, len(gridh_center)))

        for station in database.getStations("RAOB"):
            RAOB_stations.append(station)

            last_available = database.getLastRAOBSep(station.id, ep)

            temp_profile = database.getRAOBSTempAtep(station_id=station.id, ep=last_available)
            press_profile = database.getRAOBSPressAtep(station_id=station.id, ep=last_available)
            Nh_profile = database.getRAOBSNdryAtep(station_id=station.id, ep=last_available)
            
            temp_layered_profile = np.append([gridh_center], [np.interp(gridh_center, temp_profile[:,0], temp_profile[:,1])], axis=0).T
            press_layered_profile = np.append([gridh_center], [np.interp(gridh_center, press_profile[:,0], press_profile[:,1])], axis=0).T
            Nh_layered_profile = np.append([gridh_center], [np.interp(gridh_center, Nh_profile[:,0], Nh_profile[:,1])], axis=0).T

            coords = np.append(coords, station.getPLH()[0:2,:].T, axis=0)
            temp_at_coords_layer = np.empty((len(gridh_center), ))
            press_at_coords_layer = np.empty((len(gridh_center), ))
            Nh_at_coords_layer = np.empty((len(gridh_center), ))
            for i in range(0, len(gridh_center)):
                temp_at_coords_layer[i] = temp_layered_profile[i,1]
                press_at_coords_layer[i] = press_layered_profile[i,1]
                Nh_at_coords_layer[i] = Nh_layered_profile[i,1]

            temp_at_coords_layers = np.append(temp_at_coords_layers, [temp_at_coords_layer], axis=0)
            press_at_coords_layers = np.append(press_at_coords_layers, [press_at_coords_layer], axis=0)
            Nh_at_coords_layers = np.append(Nh_at_coords_layers, [Nh_at_coords_layer], axis=0)

        interp_gridp, interp_gridl =  np.meshgrid(gridp_center, gridl_center)
        temp_model_3d = np.empty((len(gridp_center), len(gridl_center), len(gridh_center)))
        press_model_3d = np.empty((len(gridp_center), len(gridl_center), len(gridh_center)))
        Nh_model_3d = np.empty((len(gridp_center), len(gridl_center), len(gridh_center)))

        for i in range(0, np.shape(temp_at_coords_layers)[1]):
            temp_layer = griddata(coords, temp_at_coords_layers[:,i], (interp_gridp.T, interp_gridl.T), method="nearest")
            press_layer = griddata(coords, press_at_coords_layers[:,i], (interp_gridp.T, interp_gridl.T), method="nearest")
            Nh_layer = griddata(coords, Nh_at_coords_layers[:,i], (interp_gridp.T, interp_gridl.T), method="nearest")
            temp_model_3d[:,:,i] = temp_layer
            press_model_3d[:,:,i] = press_layer
            Nh_model_3d[:,:,i] = Nh_layer

        for i in range(0,len(gridp_center)):
            for j in range(0,len(gridl_center)):
                sta = Little_RStation(lat=gridp_center[i], lon=gridl_center[j], alt=0.0, source="BUTE GNSS-meteorology nrt procession", epoch=ep, fm_code="FM-116")
                for k in range(0, len(gridh_center)):
                    
                    sta.add_data(P=np.array([press_model_3d[i,j,k], 0]), H=np.array([gridh_center[k], 0]), T=np.array([temp_model_3d[i,j,k], 0]), Td=np.array([Nw_model[i, j, k] + Nh_model_3d[i, j, k], 0]))
                writer.addStation(sta)
        writer.write()
        #print(model)
        #print(model)
        #output['log']['info'].append('Wet Refractivity 3D model at '+str(ep))
        #output['data']['grid']
        #output['data']['grid']['x'] = x.tolist()
        #output['data']['grid']['y'] = y.tolist()
        #output['data']['grid']['z'] = z.tolist()

except Exception as er:
    print('A')
    print(er)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    print('B')
