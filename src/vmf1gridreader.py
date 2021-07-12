#import sys
#sys.path.append('../')
import numpy as np
from scipy import interpolate
from station import Station
#from tropostation import TropoStation
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

        phi = []
        lam = []
        a_h = []
        a_w = []
        zdh = []
        zdw = []

        for r in self.grid:
            if r[0] not in phi:
                phi.append(r[0])
        for r in self.grid:
            if r[1] not in lam:
                lam.append(r[1])

        for l in lam:
            r_a_h = np.empty((1,0))
            r_a_w = np.empty((1,0))
            r_zdh = np.empty((1,0))
            r_zdw = np.empty((1,0))
            for p in phi:

                #print(np.shape(self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],2]))
                r_a_h = np.append(r_a_h, [self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],2]], axis=1)
                r_a_w = np.append(r_a_w, [self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],3]], axis=1)
                r_zdh = np.append(r_zdh, [self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],4]], axis=1)
                r_zdw = np.append(r_zdw, [self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],5]], axis=1)
            try:
                a_h = np.append(a_h, r_a_h, axis=0)
            except:
                a_h = r_a_h
            try:
                a_w = np.append(a_w, r_a_w, axis=0)
            except:
                a_w = r_a_w
            try:
                zdh = np.append(zdh, r_zdh, axis=0)
            except:
                zdh = r_zdh
            try:
                zdw = np.append(zdw, r_zdw, axis=0)
            except:
                zdw = r_zdw

        self.phi = np.array(phi)
        self.lam = np.array(lam)
        self.a_h = a_h
        self.a_w = a_w
        self.zdh = zdh
        self.zdw = zdw


    def _readBody(self):
        """read TRP body

        """
        line = self.fid.readline()

        #read stations row by row
        while line:
            if line.strip() == '':
                break


            phi = float(line[0:5])
            lam = float(line[6:11])
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
        plh = st.getPLH()[:,0]


        f = interpolate.interp2d(self.phi, self.lam, self.a_h)
        return f(plh[0]*180/np.pi, plh[1]*180/np.pi)[0]

    def getA_w(self, st):
        plh = st.getPLH()[:,0]


        f = interpolate.interp2d(self.phi, self.lam, self.a_w)
        return f(plh[0]*180/np.pi, plh[1]*180/np.pi)[0]

    def getZd_h(self, st):
        plh = st.getPLH()[:,0]


        f = interpolate.interp2d(self.phi, self.lam, self.zdh)
        return f(plh[0]*180/np.pi, plh[1]*180/np.pi)[0]

    def getZd_w(self, st):
        plh = st.getPLH()[:,0]


        f = interpolate.interp2d(self.phi, self.lam, self.zdw)
        return f(plh[0]*180/np.pi, plh[1]*180/np.pi)[0]





if __name__ == "__main__":

    reader = VMF1GridReader("../example/VMFG_20201102.H00")

    p = reader.grid[:,0]
    l = reader.grid[:,1]



    print(reader.grid[:,0])
    print(reader.grid[:,1])
    print(reader.grid[:,2])
