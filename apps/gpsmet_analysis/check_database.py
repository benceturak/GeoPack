import sys
sys.path.append("../../src")
from readdb import ReadDB
import dbconfig
import numpy as np

import epoch

db = ReadDB(dbconfig.database)


start_ep = epoch.Epoch(np.array([2021,9,20,0,0,0]))
dif_ep = epoch.Epoch(np.array([0,0,0,1,0,0]))
end_ep = epoch.Epoch(np.array([2021,9,20,2,0,0]))
ep = start_ep
sql = "SELECT DATE, TIME, STATION, COUNT(*) FROM TRPDELAY GROUP BY DATE, TIME, STATION HAVING COUNT(*) > 1"
dbcursor = dbconfig.database.cursor()

dbcursor.execute(sql)
fid = open('check_database.csv', 'w')
for line in dbcursor.fetchall():

    print(str(line[0]) + "," + str(line[1]) + "," + line[2] + "," + str(line[3]) + ";", file=fid)


exit()

for sta in db._getAllStations():
    print(sta[1])

    while ep <= end_ep:
        print(ep)

        print(date)
        print(time)
        ep = ep + dif_ep


        exit()
    #db.get
