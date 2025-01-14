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

        self.fid = open(self.fileName, 'r')
        #start read of header
        self._readFile()
        #start read of navigation datas
    
        self.fid.close()
    


    def _readFile(self):

        while True:
            line = self.fid.readline()
            if self.headerRows(line) == "EOH": break
            try:

                logging.info("header row" + line + " record is read")
            except:
                logging.warning("header row" + line + " cannot be read")
                pass
        
        while line.strip() != 'EOF':

            if line[0] == '*':
                ep = epoch.Epoch(np.array([int(line[3:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]), float(line[20:31])]))
            else:
                self.positions[line[1:4]] = np.append(self.positions[line[1:4]], np.array([[ep.GPSweek, ep.TOW, float(line[4:18])*1000, float(line[18:32])*1000, float(line[32:46])*1000, float(line[46:60])]]), axis=0)
                #print(self.positions[line[1:4]][0])
            line = self.fid.readline()

            

    def getSatellite(self, prn):
        sat = Satellite(prn)
        sat.addSP3coords(self.positions[prn])

        return sat

    def getSatellites(self, prnList=(), gnss=()):
        
        for prn in self.positions.keys():

            if (prnList == () and gnss == ()) or (prn in prnList or prn[0] in gnss):
                yield self.getSatellite(prn)
        #for prn in self.positions:
        #    yield self.getSatellite(prn)


    def headerRows(self,line):
        if line[0:2] == "#c" or line[0:2] == "#d":
            self.headerRow1(line)
            return 0
        elif line[0:2] == "##":
            self.headerRow2(line)
            return 0
        elif line[0:2] == "+ ":
            self.headerRowSats(line)
            return 0
        elif line[0:2] == "++":
            return 0
        elif line[0:2] == "%c":
            return 0
        elif line[0:2] == "%f":
            return 0
        elif line[0:2] == "%i":
            return 0
        elif line[0:2] == "/*":
            return 0
        elif line[0:2] == "* ":
            return "EOH"

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

    def headerRowSats(self,line):
        if line[4:6] != "  ":
            self.numOfSats = int(line[4:6])

        for i in range(0,17):
            if line[9+i*3:12+i*3] != "  0":
                self.positions[line[9+i*3:12+i*3]] = np.empty((0,6))

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
    def headerRow23(self,line):pass
