#!/usr/bin/python3

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
    opts, args = getopt.getopt(sys.argv[1:], 's:f:t:o:h:', ['stations=', 'from=', 'to=', 'output=', 'help'])
    stations = None



    for o, v in opts:
        if o == '--stations' or o == '-s':
            stations = v.split('|')
        elif o == '--from' or o == '-f':
            dt = v.split('-')

            fr = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
        elif o == '--to' or o == '-t':
            dt = v.split('-')

            to = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))

        elif  o == '--help' or o == '-h':
            print("Usage:")


    database = ReadDB(database=dbconfig.database)

    #fr = Epoch(np.array([2021,11,1,2,0,0]))
    #to = Epoch(np.array([2021,11,1,3,0,0]))

    output = {"data": {}, "log": {"error": [], "warning": []}}

    for i in database.getZWD(stations=stations, fr=fr, to=to):
        try:
            st = i[0]
            ep = str(i[1].dt[0])+"-"+str(i[1].dt[1])+"-"+str(i[1].dt[2])+"-"+str(i[1].dt[3])+"-"+str(i[1].dt[4])+"-"+str(i[1].dt[5])
            output["data"][st][ep] = i[2]
        except KeyError:
            output["data"][st] = {}
            output["data"][st][ep] = i[2]


except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"].append("Error")
    #print(er)

print(json.dumps(output))
