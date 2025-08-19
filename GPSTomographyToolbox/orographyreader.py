#import sys
#sys.path.append('../')
import numpy as np
from scipy import interpolate
from station import Station
#from tropostation import TropoStation
import epoch

class OrographyReader(object):

    """!OrographyReader class to read Orography grid file

            
    """

    def __init__(self, fileName):
        """OrograpgyReader initializer
        @param fileName (string): name of Orography file 

        """

        self.fileName = fileName#filename

        self.grid = np.empty((0,))

        self.epochs = np.empty((0,))

        try:
            self.fid = open(fileName, 'r')

            #start read of header
            self._readHeader()
            #start read of stations
            self._readBody()
        finally:
            self.fid.close()



    def _readBody(self):
        """!read orography file body

        """
        line = self.fid.readline()



        #read stations row by row
        grid = np.empty((0,6))
        row = np.empty((0,))
        while line:

            for i in range(0,10):
                try:
                    row = np.append(row, float(line[0+i*8:8+i*8]))
                except:
                    try:
                        self.grid = np.append(self.grid, [row], axis=0)
                    except ValueError as er:
                        self.grid = np.array([row])
                    row = np.empty((0,))
                    break





            #grid = np.append(grid, r, axis=0)



            #read satellite navigation datas in a valid epoch
            #self._readEpochSatNav(line)
            line = self.fid.readline()


    def _readHeader(self):
        """!read Orography header

        """

        #read Bernese TRP file header row by row


        line = self.fid.readline()#read row
        self.p_min = float(line[3:10])
        self.p_max = float(line[11:20])
        self.l_min = float(line[23:31])
        self.l_max = float(line[32:38])
        self.p_d = float(line[40:48])
        self.l_d = float(line[50:])

        self.phi = np.arange(self.p_min, self.p_max-self.p_d, -self.p_d)
        self.lam = np.arange(self.l_min, self.l_max+self.l_d, self.l_d)

    def getOro(self, st):
        """!get orography at the given station
        @param st (Point, Station): station
        """
        plh = st.getPLH()[:,0]


        f = interpolate.interp2d(self.phi, self.lam, self.grid.T)

        return f(plh[0]*180/np.pi, plh[1]*180/np.pi)





if __name__ == "__main__":

    filename = "../data/tomography/2021/orography_ell"

    reader = OrographyReader(filename)

    p = reader.grid[:,0]
    l = reader.grid[:,1]

    from ellipsoid import WGS84
    sta = Station(coord=np.array([47*np.pi/180,19*np.pi/180,100]), type=2, system=WGS84())

    print(reader.getOro(sta))
    #print(reader.grid[:,1])
    #print(reader.grid[:,2])
