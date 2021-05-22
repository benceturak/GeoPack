import epoch
import numpy as np

class SP3Reader(object):

    def __init__(self, fileName):
        """SP3Reader condtructor

        """

        self.fileName = fileName#filename
        self.comments = []#comment records
        self.numOfSats = 0
        self.positions = np.empty((0,2))
        try:
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
            #start read of navigation datas
            self._readBody()
        finally:
            self.fid.close()

    def _readHeader(self):

        for i in range(1, 23):
            line = self.fid.readline()
            try:
                eval('headerRow'+str(i)+"(line)")
                logging.info("header row" + i + " record is readed")
            except:
                logging.warning("header row" + i + " cannot be readed")
                pass

    def headerRow1(self,line):
        self.version = line[1]
        self.posVerFlag = self.startDate = epoch.Epoch(np.array([int(line[3:7]), int(line[8:10]), int(line[11:13]), int(line[14:16]), int(line[17:19]), float(line[20:31])]))
        self.numOfEpochs = int(line[32:39])

    def headerRow2(self,line):pass
    def headerRow3(self,line):pass
    def headerRow4(self,line):pass
    def headerRow5(self,line):pass
    def headerRow6(self,line):pass
    def headerRow7(self,line):pass
    def headerRow8(self,line):pass
    def headerRow9(self,line):pass
    def headerRow10(self,line):pass
    def headerRow11(self,line):pass
    def headerRow12(self,line):pass
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
