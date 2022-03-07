#!/usr/bin/python3
output = {"data": {"data": {},"grid": {"x": [], "y": [], "z": []}}, "log": {"error": [], "warning": [], "info": []}}
try:
    import sys
    import traceback

    sys.path.append("/home/bence/data/GeoPack/src")
    from readdb import ReadDB
    from epoch import Epoch
    import dbconfig
    import numpy as np
    import getopt
    import importlib
    import json
    opts, args = getopt.getopt(sys.argv[1:], 'e:h:T:m:', ['epoch=', 'type=', 'method=', 'help'])
    stations = None
    type = "Nw"
    kind = "linear"


    for o, v in opts:
        if o == '--epoch' or o == '-e':
            dt = v.split('-')
            ep = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
        elif o == '--type' or o == '-T':
            type = v
        elif  o == '--help' or o == '-h':
            print("Usage:")


    database = ReadDB(database=dbconfig.database)

    #fr = Epoch(np.array([2021,11,1,2,0,0]))
    #to = Epoch(np.array([2021,11,1,3,0,0]))

    if type == 'Nw' or type == 'NW':
        model, x, y, z = database.getNwAtEp(ep)
        #print(model)
        output['log']['info'].append('Wet Refractivity 3D model at '+str(ep))
        output['data']['grid']
        output['data']['grid']['x'] = x.tolist()
        output['data']['grid']['y'] = y.tolist()
        output['data']['grid']['z'] = z.tolist()

    for i in range(0, np.shape(z)[0]):
        output["data"]["data"].update({z[i]: {}})
        for j in range(0, np.shape(x)[0]):
            output["data"]["data"][z[i]].update({x[j]: {}})
            for k in range(0, np.shape(y)[0]):
                output["data"]["data"][z[i]][x[j]].update({y[k]: model[j,k,i]})



except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"]['error'].append(str(er))
    #print(er)

print(json.dumps(output))
