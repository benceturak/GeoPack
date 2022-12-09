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
    opts, args = getopt.getopt(sys.argv[1:], 'h:t:', ['type=', 'help'])
    stations = None


    type = None
    for o, v in opts:
        if o == '--type' or o == '-t':
            type = v.split('|')
        elif  o == '--help' or o == '-h':
            print("Usage:")

    if type == ['',]:
        type = None



    database = ReadDB(database=dbconfig.database)




    for i in database.getStations(type):

        output['data'].append({'id': i.id, 'coords': [i.getPLH()[0,0],i.getPLH()[1,0],i.getPLH()[2,0]], 'network': i.code})




except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"]['error'].append(str(er))
    #print(er)

print(json.dumps(output))
