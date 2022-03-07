#!/usr/bin/python3
import numpy as np
import json
import sys
import traceback
output = {"data": {}, "log": {"error": [], "warning": [], "info": []}}

try:

    gridp = np.loadtxt("/home/bence/data/GeoPack/apps/gpsmet_analysis/gridp.csv")
    gridl = np.loadtxt("/home/bence/data/GeoPack/apps/gpsmet_analysis/gridl.csv")
    #gridh = np.loadtxt(gridh_file)


    for i in range(0, np.shape(gridp)[0]-1):
        pc = (gridp[i] + gridp[i+1])/2
        output['data'].update({pc: {}})

        for j in range(0, np.shape(gridl)[0]-1):
            lc = (gridl[j] + gridl[j+1])/2

            output['data'][pc].update({lc: ((gridp[i], gridl[j]),(gridp[i], gridl[j+1]),(gridp[i+1], gridl[j+1]),(gridp[i+1], gridl[j]))})
except Exception as er:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
    #print(exc_type)
    output["log"]['error'].append(str(er))
    #print(er)


print(json.dumps(output))
