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

    def __init__(self, fileNames):
        """VMF1GridReader constructor

        """

        self.fileNames = fileNames#filename

        self.grid = np.empty((0,))
        self.phi = 0
        self.lam = 0
        #self.network = Network()
        #self.comments = []#comment records
        #self.navigationDatas = {}#navigation datas
        self.epochs = np.empty((0,))
        for fileName in fileNames:
            try:
                self.fid = open(fileName, 'r')
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

            grid = self.grid[-1,:,:]
            for r in grid:
                if r[0] not in phi:
                    phi.append(r[0])
            for r in grid:
                if r[1] not in lam:
                    lam.append(r[1])

            for l in lam:
                r_a_h = np.empty((1,0))
                r_a_w = np.empty((1,0))
                r_zdh = np.empty((1,0))
                r_zdw = np.empty((1,0))
                for p in phi:

                    #print(np.shape(self.grid[np.where(np.all([p == self.grid[:,0],l == self.grid[:,1]], axis=0))[0],2]))
                    r_a_h = np.append(r_a_h, [grid[np.where(np.all([p == grid[:,0],l == grid[:,1]], axis=0))[0],2]], axis=1)
                    r_a_w = np.append(r_a_w, [grid[np.where(np.all([p == grid[:,0],l == grid[:,1]], axis=0))[0],3]], axis=1)
                    r_zdh = np.append(r_zdh, [grid[np.where(np.all([p == grid[:,0],l == grid[:,1]], axis=0))[0],4]], axis=1)
                    r_zdw = np.append(r_zdw, [grid[np.where(np.all([p == grid[:,0],l == grid[:,1]], axis=0))[0],5]], axis=1)
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

            if self.phi == 0:
                self.phi = phi
                self.lam = lam

            try:

                self.a_h = np.append(self.a_h, [a_h], axis=0)
                self.a_w = np.append(self.a_w, [a_w], axis=0)
                self.zdh = np.append(self.zdh, [zdh], axis=0)
                self.zdw = np.append(self.zdw, [zdw], axis=0)
            except Exception as er:
                self.a_h = np.array([a_h])

                self.a_w = np.array([a_w])
                self.zdh = np.array([zdh])
                self.zdw = np.array([zdw])

    def _readBody(self):
        """read TRP body

        """
        line = self.fid.readline()

        #read stations row by row
        grid = np.empty((0,6))
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


            grid = np.append(grid, r, axis=0)



            #read satellite navigation datas in a valid epoch
            #self._readEpochSatNav(line)
            line = self.fid.readline()
        try:
            self.grid = np.append(self.grid, [grid], axis=0)
        except ValueError as er:
            self.grid = np.array([grid])

    def _readHeader(self):
        """read TRP header

        """

        #read Bernese TRP file header row by row
        for i in range(0,7):

            line = self.fid.readline()#read row
            print(line)

            if i == 3:
                year = int(line[22:26])
                month = int(line[27:29])
                day = int(line[30:32])
                hour = int(line[33:35])
                min = int(line[36:38])
                sec = float(line[39:])


                self.epochs = np.append(self.epochs, epoch.Epoch(np.array([year,month,day,hour,min,sec])).MJD)
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

    def getA_h(self, st, ep):
        plh = st.getPLH()[:,0]

        i = np.where(np.abs(self.epochs - ep.MJD) <= 0.25)[0]

        if len(i) == 1 and self.epochs == ep.MJD:
            f = interpolate.interp2d(self.phi, self.lam, self.a_h[i[0],:,:])
            return f(plh[0]*180/np.pi, plh[1]*180/np.pi)
        elif len(i) == 2:

            f1 = interpolate.interp2d(self.phi, self.lam, self.a_h[i[0],:,:])
            f2 = interpolate.interp2d(self.phi, self.lam, self.a_h[i[1],:,:])


            t = self.epochs[i]
            v = np.append(f1(plh[0]*180/np.pi, plh[1]*180/np.pi), f2(plh[0]*180/np.pi, plh[1]*180/np.pi))
            f = interpolate.interp1d(t, v)
            return f(ep.MJD)
        else:
            raise epoch.TimeError('Invalid epoch (out of timeinterval)')

    def getA_w(self, st, ep):
        plh = st.getPLH()[:,0]

        i = np.where(np.abs(self.epochs - ep.MJD) <= 0.25)[0]

        if len(i) == 1 and self.epochs == ep.MJD:
            f = interpolate.interp2d(self.phi, self.lam, self.a_w[i[0],:,:])
            return f(plh[0]*180/np.pi, plh[1]*180/np.pi)
        elif len(i) == 2:

            f1 = interpolate.interp2d(self.phi, self.lam, self.a_w[i[0],:,:])
            f2 = interpolate.interp2d(self.phi, self.lam, self.a_w[i[1],:,:])


            t = self.epochs[i]
            v = np.append(f1(plh[0]*180/np.pi, plh[1]*180/np.pi), f2(plh[0]*180/np.pi, plh[1]*180/np.pi))
            f = interpolate.interp1d(t, v)
            return f(ep.MJD)
        else:
            raise epoch.TimeError('Invalid epoch (out of timeinterval)')

    def getZhd(self, st, ep):
        plh = st.getPLH()[:,0]

        i = np.where(np.abs(self.epochs - ep.MJD) <= 0.25)[0]

        if len(i) == 1 and self.epochs == ep.MJD:
            f = interpolate.interp2d(self.phi, self.lam, self.zdh[i[0],:,:])
            return f(plh[0]*180/np.pi, plh[1]*180/np.pi)
        elif len(i) == 2:

            f1 = interpolate.interp2d(self.phi, self.lam, self.zdh[i[0],:,:])
            f2 = interpolate.interp2d(self.phi, self.lam, self.zdh[i[1],:,:])


            t = self.epochs[i]
            v = np.append(f1(plh[0]*180/np.pi, plh[1]*180/np.pi), f2(plh[0]*180/np.pi, plh[1]*180/np.pi))
            f = interpolate.interp1d(t, v)
            return f(ep.MJD)
        else:
            raise epoch.TimeError('Invalid epoch (out of timeinterval)')

    def getZwd(self, st, ep):
        plh = st.getPLH()[:,0]

        i = np.where(np.abs(self.epochs - ep.MJD) <= 0.25)[0]

        if len(i) == 1 and self.epochs == ep.MJD:
            f = interpolate.interp2d(self.phi, self.lam, self.zdw[i[0],:,:])
            return f(plh[0]*180/np.pi, plh[1]*180/np.pi)
        elif len(i) == 2:

            f1 = interpolate.interp2d(self.phi, self.lam, self.zdw[i[0],:,:])
            f2 = interpolate.interp2d(self.phi, self.lam, self.zdw[i[1],:,:])


            t = self.epochs[i]
            v = np.append(f1(plh[0]*180/np.pi, plh[1]*180/np.pi), f2(plh[0]*180/np.pi, plh[1]*180/np.pi))
            f = interpolate.interp1d(t, v)
            return f(ep.MJD)*np.exp(-plh[2]/2000)
        else:
            raise epoch.TimeError('Invalid epoch (out of timeinterval)')





if __name__ == "__main__":

    filenames = ["../example/VMFG_20201102.H00", "../example/VMFG_20201102.H06"]#, "../example/VMFG_20201102.H12", "../example/VMFG_20201102.H18"]

    reader = VMF1GridReader(filenames)

    p = reader.grid[:,0]
    l = reader.grid[:,1]

    from ellipsoid import WGS84
    sta = Station(coord=np.array([np.pi/2,np.pi/2,100]), type=2, system=WGS84())

    ep = epoch.Epoch(np.array([2020,11,2,0,0,0]))


    #print(reader.epochs)
    print(reader.getA_h(sta, ep))
    #print(reader.grid[:,1])
    #print(reader.grid[:,2])
