import epoch
import numpy as np
import logging
from satellite import Satellite

class SP3Reader(object):

    def __init__(self, fileName):
        """SP3Reader condtructor

        """

        self.fileName = fileName#filename
        self.comments = []#comment records
        self.numOfSats = 0
        self.positions = {}
        self.accuracy = []
        #self.positions = np.empty((0,2))
        try:
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
            #start read of navigation datas
            self._readBody()
        finally:
            self.fid.close()
    def _readBody(self):
        #print(self.positions)
        line = self.fid.readline()
        while line.strip() != 'EOF':

            if line[0] == '*':
                ep = epoch.Epoch(np.array([int(line[3:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]), float(line[20:31])]))
            else:
                self.positions[line[1:4]] = np.append(self.positions[line[1:4]], np.array([[ep, float(line[4:18])*1000, float(line[18:32])*1000, float(line[32:46])*1000, float(line[46:60])]]), axis=0)
                #print(self.positions[line[1:4]][0])
                #print(np.shape(self.positions[line[1:4]]))
            line = self.fid.readline()


    def _readHeader(self):

        for i in range(1, 23):
            line = self.fid.readline()
            eval('self.headerRow'+str(i)+"(line)")
            try:

                logging.info("header row" + str(i) + " record is readed")
            except:
                logging.warning("header row" + str(i) + " cannot be readed")
                pass

    def getSatellite(self, prn):
        sat = Satellite(prn)
        sat.addSP3coords(self.positions[prn])

        return sat

    def getSatellites(self):
        for prn in self.positions:
            yield self.getSatellite(prn)



    def headerRow1(self,line):
        self.version = line[1]
        self.posVerFlag = line[2]
        self.startDate = epoch.Epoch(np.array([int(line[3:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]), float(line[20:31])]))
        self.numOfEpochs = int(line[32:39])
        self.dataUsed = line[40:45].strip()
        self.coordinateSystem = line[46:51].strip()
        self.orbitType = line[52:55].strip()
        self.agency = line[56:60].strip()


    def headerRow2(self,line):
        self.GPSweek = int(line[3:7])
        self.secondsOfWeek = float(line[8:23])
        self.epochInterval = float(line[24:38])
        self.MDF = int(line[39:44])
        self.fractionalDay = float(line[45:60])

    def headerRow3(self,line):
        self.numOfSats = int(line[4:6])

        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,5))

    def headerRow4(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,5))
    def headerRow5(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,5))
    def headerRow6(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,5))
    def headerRow7(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,5))
    def headerRow8(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.accuracy.append(line[9+i*3:12+i*3])
    def headerRow9(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.accuracy.append(line[9+i*3:12+i*3])
    def headerRow10(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.accuracy.append(line[9+i*3:12+i*3])
    def headerRow11(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.accuracy.append(line[9+i*3:12+i*3])
    def headerRow12(self,line):
        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.accuracy.append(line[9+i*3:12+i*3])
    def headerRow13(self,line):pass


    def headerRow14(self,line):pass
    def headerRow15(self,line):pass
    def headerRow16(self,line):pass
    def headerRow17(self,line):pass
    def headerRow18(self,line):pass
    def headerRow19(self,line):pass
    def headerRow20(self,line):pass
    def headerRow21(self,line):pass
    def headerRow22(self,line):pass
