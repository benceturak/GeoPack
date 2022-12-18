#!/usr/bin/python3
output = {"data": [], "log": {"error": [], "warning": [], "info": []}}
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
    #opts, args = getopt.getopt(sys.argv[1:], 'p:l:e:h:T:m:', ['phi=', 'lam=', 'epoch=', 'type=', 'method=', 'help'])
    #stations = None
    #type = "Nw"
    #kind = "linear"


    #for o, v in opts:
    #    if o == '--phi' or o == '-p':
    #        lat = float(v)
    #    elif o == '--lam' or o == '-l':
    #        lon = float(v)
    #    elif o == '--epoch' or o == '-e':
    #        dt = v.split('-')

    #        ep = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
    #    elif o == '--type' or o == '-T':
    #        type = v
    #    elif o == '--method' or o == '-m':
    #        kind = v
    #    elif  o == '--help' or o == '-h':
    #        print("Usage:")


    database = ReadDB(database=dbconfig.database)

    #fr = Epoch(np.array([2021,11,1,2,0,0]))
    #to = Epoch(np.array([2021,11,1,3,0,0]))



    for i in database.getStations():

        output['data'].append({'id': i.id, 'coords': [i.getPLH()[0,0],i.getPLH()[1,0],i.getPLH()[2,0]], 'network': i.code, 'location': i.other})




except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"]['error'].append(str(er))
    #print(er)

print(json.dumps(output))
