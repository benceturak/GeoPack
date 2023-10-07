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
    opts, args = getopt.getopt(sys.argv[1:], 'w:d:h:f:', ['week=', 'datumid=', 'file=', 'help'])

    for o, v in opts:
        if o == '--week' or o == '-w':
            week = int(v)
        elif o == '--datumid' or o == '-d':
            datum = int(v)
        elif o == '--file' or o == '-f':
            filename = v
        elif  o == '--help' or o == '-h':
            print("Usage:")


    database = ReadDB(database=dbconfig.database)

    #fr = Epoch(np.array([2021,11,1,2,0,0]))
    #to = Epoch(np.array([2021,11,1,3,0,0]))

    #if type == 'Nw' or type == 'NW':
    #    profile = database.getNwProfile(lat, lon, ep, kind)
    #    output['log']['info'].append('Wet Refractivity(Nw) profile at '+str(ep))
    #elif type == 'WVD' or type == 'wvd':
    #    profile = database.getWVDProfile(lat, lon, ep, kind)
    #    output['log']['info'].append('Wet Refractivity(Nw) profile at '+str(ep))

    #z = []
    #val = []
    fid = open(filename, "w")

    IDs, coords = database.getWeeklyCoords(week, datum)
        
        #output["data"].append((row[0], row[1]))
    for i in range(0,len(IDs)):
        line = "{:4s} {:4d} {:13.5f} {:13.5f} {:13.5f} {:1d}".format(IDs[i], int(coords[i,0]), coords[i,1], coords[i,2], coords[i,3], int(coords[i,4]))
        print(line, file=fid)

    fid.close()



except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"]['error'].append(str(er))
    #print(er)

#print(json.dumps(output))
