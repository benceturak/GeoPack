#!/usr/bin/python3

import sys
import traceback

sys.path.append("/home/bence/data/GeoPack/src")
from readdb import ReadDB
from epoch import Epoch
import dbconfig
import numpy as np

import getopt
opts, args = getopt.getopt(sys.argv[1:], 'e:o:', ['epoch=', 'out='])


for o, v in opts:
    if o == '--epoch' or o == '-e':
        dt = v.split('-')
        ep = Epoch(np.array([int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3]),int(dt[4]),int(dt[5])]))
    elif o == '--out' or o == '-o':
        fname = v
    elif  o == '--help' or o == '-h':
        print("Usage:")


database = ReadDB(database=dbconfig.database)

(Nw, x, y, z) = database.getNwAtEp(Epoch(np.array([2022,3,16,11,0,0])))

print(Nw)
print(fname)
np.save(fname, Nw)

#fr = Epoch(np.array([2021,11,1,2,0,0]))
#to = Epoch(np.array([2021,11,1,3,0,0]))
