#import sys
#sys.path.append('../')
import numpy as np
from scipy import interpolate
from station import Station
from tropostation import TropoStation
import epoch

class VMF1GridReader(object):

    """
        VMF1GridReader class to read VMF1 (Vienna Mapping Function) grid file format file

            :param fileName: name of VMF1 file (string)
    """

    def __init__(self, fileName):
        """VMF1GridReader constructor

        """

        self.fileName = fileName#filename

        self.grid = np.empty((0,6))
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


            phi = float(line[1:5])
            lam = float(line[7:11])
            a_h = float(line[12:22])
            a_w = float(line[23:34])
            d_h = float(line[35:42])
            d_w = float(line[43:50])


            r = np.array([[phi, lam, a_h, a_w, d_h, d_w]])


            self.grid = np.append(self.grid, r, axis=0)



            #read satellite navigation datas in a valid epoch
            #self._readEpochSatNav(line)
            line = self.fid.readline()

    def _readHeader(self):
        """read TRP header

        """

        #read Bernese TRP file header row by row
        for i in range(0,7):

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

    def getA_h(self, st):
        plh = st.getPLH()

        f = interpolate.interp2d(reader.grid[:,0], reader.grid[:,1], reader.grid[:,2])

        return = f(plh[0]*180/np.pi, plh[1]*180/np.pi)

    def getA_w(self, st):
        plh = st.getPLH()

        f = interpolate.interp2d(reader.grid[:,0], reader.grid[:,1], reader.grid[:,3])

        return = f(plh[0]*180/np.pi, plh[1]*180/np.pi)

    def getZd_h(self, st):
        plh = st.getPLH()

        f = interpolate.interp2d(reader.grid[:,0], reader.grid[:,1], reader.grid[:,4])

        return = f(plh[0]*180/np.pi, plh[1]*180/np.pi)

    def getZd_w(self, st):
        plh = st.getPLH()

        f = interpolate.interp2d(reader.grid[:,0], reader.grid[:,1], reader.grid[:,5])

        return = f(plh[0]*180/np.pi, plh[1]*180/np.pi)





if __name__ == "__main__":

    reader = VMF1GridReader("../example/VMFG_20201102.H00")

    p = reader.grid[:,0]
    l = reader.grid[:,1]



    print(reader.grid[:,0])
    print(reader.grid[:,1])
    print(reader.grid[:,2])
