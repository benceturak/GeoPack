import sys
sys.path.append('../')
import numpy as np
from station import Station
from tropostation import TropoStation
import epoch

class ReadTRP(object):
    """
        ReadTRP class to read Bernese TRP (troposphere) format file

            :param fileName: name of TRP file (string)
    """

    def __init__(self, fileName):
        """ReadTRP constructor

        """

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
            ep = epoch.Epoch(np.array([year,month,day,hour,min,sec]), epoch.GPS)

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
            print(line)
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

    def getTropoByStationEpoch(self, digit4Id, ep):


        return self.troposphere[digit4Id][np.where(self.troposphere[digit4Id][:,0] == ep)[0],:]






if __name__ == "__main__":

    reader = ReadTRP("../../example/CO21173H.TRP")
    id = 'BAIA'
    ep = epoch.Epoch(np.array([2021,6,22,3,0,0]), system=epoch.GPS)

    print(np.shape(reader.getTropoByStationEpoch(id, ep)))
