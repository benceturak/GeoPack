import sys
sys.path.append('../')
import numpy as np
from station import Station
from network import Network
from ellipsoid import WGS84

class ReadCRD(object):
    """
        ReadCRD class to read Bernese CRD format file

            :param fileName: name of CRD file (string)
    """

    def __init__(self, fileName):
        """ReadCRD constructor

        """

        self.fileName = fileName#filename
        self.network = Network()
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
        """read CRD body

        """
        line = self.fid.readline()

        #read stations row by row
        while line:
            if line.strip() == '':
                break


            numId = line[0:3]
            digit4Id = line[5:9]
            dom = line[11:21]
            x = float(line[22:36])
            y = float(line[37:51])
            z = float(line[52:66])
            flag = line[68:]

            st = Station(id=digit4Id, code=numId, coord=np.array([[x,y,z]]),system=WGS84())

            self.network.addStation(st)





            #read satellite navigation datas in a valid epoch
            #self._readEpochSatNav(line)
            line = self.fid.readline()

    def _readHeader(self):
        """read CRD header

        """

        #read Bernese CRD file header row by row
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

if __name__ == "__main__":

    reader = ReadCRD("../../example/BME001.CRD")

    print(reader.network.getStationsMatrix())


    #print(reader.beta)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
