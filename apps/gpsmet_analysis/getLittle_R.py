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
    opts, args = getopt.getopt(sys.argv[1:], 's:f:t:o:h:', ['stations=', 'from=', 'to=', 'output=', 'help'])
    stations = None



    for o, v in opts:
        if o == '--stations' or o == '-s':
            stations = v.split(',')
        elif o == '--from' or o == '-f':
            dt = v.split('-')

            fr = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
        elif o == '--to' or o == '-t':
            dt = v.split('-')

            to = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
        elif o == '--output' or o == '-o':
            filename = v

        elif  o == '--help' or o == '-h':
            print("Usage:")


    database = ReadDB(database=dbconfig.database)



    #fr = Epoch(np.array([2021,11,1,2,0,0]))
    #to = Epoch(np.array([2021,11,1,3,0,0]))
    writer = Little_RWriter(filename)

    for i in database.getZTD(stations=stations, fr=fr, to=to):
        try:
            p = database.getStation(i[0])
            plh = p.getPLH()[:,0]
            sta = Little_RStation(lat=plh[0], lon=plh[1], alt=plh[2], id=p.id, name=p.id, source="BUTE GNSS-meteorology nrt procession", epoch=i[1])
            sta.setZTD(i[2])
            writer.addStation(sta)
        except ValueError as er:
            print(er)

    writer.write()

except Exception as er:
    print('A')
    print(er)
    #print(traceback.format_exec())
    print('B')
