import sys
sys.path.append('../')
import numpy as np
from station import Station
#from tropostation import TropoStation
import epoch
from scipy import interpolate

TXT = 1
DB = 2


class ReadTRP(object):
    """
        ReadTRP class to read Bernese TRP (troposphere) format file

            :param fileName: name of TRP file (string)
    """

    def __init__(self, fileName=None, database=None, table=None, type=TXT):
        """ReadTRP constructor

        """
        if type == TXT:
            self.fileName = fileName#filename

            self.troposphere = {}
            #self.network = Network()
            #self.comments = []#comment records
            #self.navigationDatas = {}#navigation datas
            #self.tauC = epoch.Epoch(np.array([0, 0, 0, 0, 0, 0]))
            try:
                self.fid = open(self.fileName, 'r')
                #start read of header
                self._readHeader()
                #start read of stations
                self._readBody()
            finally:
                self.fid.close()
        elif type == DB:
            self.database = database.cursor()
            self.table = table

        self.type = type



    def _readBody(self):
        """read TRP body

        """
        line = self.fid.readline()

        #read stations row by row
        while line:
            if line.strip() == '':
                break

            digit4Id = line[1:5]
            #dom = line[11:21]
            year = int(line[24:28])
            month = int(line[29:31])
            day = int(line[32:34])
            hour = int(line[35:37])
            min = int(line[38:40])
            sec = int(line[41:43])
            ep = epoch.Epoch(np.array([year,month,day,hour,min,sec]), epoch.GPS).MJD

            #print(ep)

            mod_u = float(line[67:74].strip())
            corr_u = float(line[75:83].strip())
            sigma_u = float(line[83:91].strip())
            total_u = float(line[91:99].strip())
            corr_n = float(line[99:108].strip())
            sigma_n = float(line[108:116].strip())
            corr_e = float(line[117:126].strip())
            sigma_e = float(line[126:134].strip())

            r = np.array([[ep, mod_u, corr_u, sigma_u, total_u, corr_n, sigma_n, corr_e, sigma_e]])


            try:
                self.troposphere[digit4Id] = np.append(self.troposphere[digit4Id], r, axis=0)
            except KeyError:
                self.troposphere[digit4Id] = r



            #read satellite navigation datas in a valid epoch
            #self._readEpochSatNav(line)
            line = self.fid.readline()

    def _readHeader(self):
        """read TRP header

        """

        #read Bernese TRP file header row by row
        for i in range(0,6):

            line = self.fid.readline()#read row
            continue

            type = line[60:].replace("/","_").replace(":","_").replace("-","_").replace("#","").replace(",","").replace(" ","").replace("\n","")#replace special chars in title


            try:
                #read header record
                eval("self."+type+"(line)")
                logging.info(line[60:].strip() + " record is readed")
            except AttributeError as er:
                logging.warning(line[60:].strip() + " cannot be readed")

            if type == 'ENDOFHEADER':
                break

    def get_MOD_U(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,1])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT ZHD FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)


    def get_CORR_U(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,2])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT ZWD FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                print(params)
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_SIGMA_U(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,3])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT SIGMA_ZWD FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                print(params)
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_TOTAL_U(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,4])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT ZTD FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])

                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)
                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')


                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_CORR_N(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,5])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT GRAD_N FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                print(params)
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_SIGMA_N(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,6])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT SIGMA_GRAD_N FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                print(params)
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_CORR_E(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,7])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT GRAD_E FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                print(params)
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)

    def get_SIGMA_E(self, digit4Id, ep):
        if self.type == TXT:
            f = interpolate.interp1d(self.troposphere[digit4Id][:,0], self.troposphere[digit4Id][:,8])
            return f(ep.MJD)
        elif self.type == DB:
            sql = 'SELECT SIGMA_GRAD_E FROM TRPDELAY WHERE STATION=%s AND DATE=%s AND TIME=%s AND constellation=0;'
            if ep.dt[4] == 0 and ep.dt[5] == 0:
                dt = str(ep).split(' ')
                params = (digit4Id, dt[0], dt[1])
                self.database.execute(sql, params)
                res = self.database.fetchall()
                return res[0][0]
            else:
                ep_min = ep.floor(3)
                ep_max = ep.ceil(3)

                dt_min = str(ep_min).split(' ')
                dt_max = str(ep_max).split(' ')

                params = [(digit4Id, dt_min[0], dt_min[1]), (digit4Id, dt_max[0], dt_max[1])]
                self.database.execute(sql, params[0])
                res1 = self.database.fetchall()
                self.database.execute(sql, params[1])
                res2 = self.database.fetchall()

                f = interpolate.interp1d((ep_min.MJD, ep_max.MJD), (res1[0][0], res2[0][0]))
                return f(ep.MJD)





    def getTropoByStationEpoch(self, digit4Id, ep):


        return self.troposphere[digit4Id][np.where(self.troposphere[digit4Id][:,0] == ep)[0],:]






if __name__ == "__main__":
    import mysql.connector

    database = mysql.connector.connect(
    host = 'localhost',
    user='user',
    password='password',
    database='database'
    )

    reader = ReadTRP(database = database, table = 'TRPDELAY',type=DB)
    id = 'BAIA'
    ep = epoch.Epoch(np.array([2021,9,30,3,30,0]), system=epoch.GPS)

    print(reader.get_MOD_U(id, ep))
