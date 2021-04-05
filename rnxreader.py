import numpy as np
import math

class RNXReader(object):

    def __init__(self, fileName):

        self.fileName = fileName
        self.comments = []
        self.observationTypes = []
        self.numberOfObservationTypes = 0
        self.observations = {}
        try:
            self.fid = open(self.fileName, 'r')

            self._readHeader()

        finally:
            self.fid.close()

    def getValidTimeFrame(self):
        pass

    def readObservations(self):
        line = self.fid.readline()

        i = 1
        while line:
            i = i + 1
            #print(line)
            self._readEpochSats(line)
            line = self.fid.readline()


    def _readEpochSats(self, line):

        listOfSats = []

        if int(line[1:3]) > 80:
            year = 1900 + int(line[1:3])
        else:
            year = 2000 + int(line[1:3])

        month = int(line[1:3])

        month = int(line[4:6])
        day = int(line[7:9])
        hour = int(line[10:12])
        min = int(line[13:15])
        sec = float(line[15:26])

        epoch = np.array([[year, month, day, hour, min, sec]])

        epochFlag = int(line[28:29])

        numOfSats = int(line[29:32])


        rows = int((numOfSats-1)/12)


        resid = numOfSats%12

        if resid == 0:
            resid = 12


        for j in range(rows):
            [listOfSats.append(line[32+i*3:35+i*3].replace(" ", "0")) for i in range(12)]
            line = self.fid.readline()

        [listOfSats.append(line[32+i*3:35+i*3].replace(" ", "0")) for i in range(resid)]

        for i in range(numOfSats):
            sat = listOfSats[i]


            if sat in self.observations.keys():
                self.observations[sat] = np.append(self.observations[sat], self._readObs(epoch), axis=0)
            else:
                self.observations[sat] = self._readObs(epoch)



    def _readObs(self, epoch):
        obsRows = int(self.numberOfObservationTypes / 5)
        obsResid = self.numberOfObservationTypes % 5


        for i in range(obsRows):
            line = self.fid.readline()
            for j in range(5):
                block = line[0+j*16:16+j*16]

                if block[0:14].strip() == '':
                    obs = 0
                else:
                    obs = float(block[0:14])

                if block[14:15].strip() == '':
                    LLI = 0
                else:
                    LLI = int(block[14:15])

                if block[15:16].strip() == '':
                    sigStr = 0
                else:
                    sigStr = int(block[15:16])

                epoch = np.append(epoch, [[obs, LLI, sigStr]], axis=1)

        line = self.fid.readline()
        for j in range(obsResid):
            block = line[0+j*16:16+j*16]


            if block[0:14].strip() == '':
                obs = 0
            else:
                obs = float(block[0:14])

            if block[14:15].strip() == '':
                LLI = 0
            else:
                LLI = int(block[14:15])

            if block[15:16].strip() == '':
                sigStr = 0
            else:
                sigStr = int(block[15:16])

            epoch = np.append(epoch, [[obs, LLI, sigStr]], axis=1)

        return epoch



    def _readHeader(self):

        while True:

            line = self.fid.readline()

            type = line[60:].replace("/","_").replace(":","_").replace("#","").replace(" ","").replace("\n","")


            try:
                print("self."+type+"(line)")
                eval("self."+type+"(line)")
            except AttributeError as er:
                print(er)

            if type == 'ENDOFHEADER':
                break


    def RINEXVERSION_TYPE(self, line):
        version = line[0:9].replace(" ","").split(".")

        version_1 = int(version[0])
        version_2 = int(version[1])

        self.version = np.array([version_1, version_2])
        self.fileType = line[20:21].replace(" ","")

        self.satSystem = line[40:41].replace(" ","")

    def COMMENT(self,line):
        self.comments.append(line[0:60].strip())

    def PGM_RUNBY_DATE(self, line):
        self.programName = line[0:20].strip()
        self.agencyName = line[20:40].strip()
        self.date = line[40:60].strip()

    def MARKERNAME(self, line):
        self.markerName = line[0:60].strip()

    def MARKERNUMBER(self, line):
        self.markerNumber = line[0:20].strip()

    def OBSERVER_AGENCY(self, line):
        self.observerName = line[0:20].strip()
        self.agency = line[20:60].strip()

    def REC_TYPE_VERS(self, line):
        self.receiverNumber = line[0:20].strip()
        self.receiverType = line[20:40].strip()
        self.receiverVersion = line[40:60].strip()

    def ANT_TYPE(self, line):
        self.antennaNumber = line[0:20].strip()
        self.antennaType = line[20:40].strip()

    def APPROXPOSITIONXYZ(self, line):

        self.approxPosition = np.array([float(line[0:14]), float(line[14:28]), float(line[28:42])])

    def ANTENNA_DELTAH_E_N(self, line):
        self.eccenctrities = np.array([float(line[0:14]), float(line[14:28]), float(line[28:42])])



    def _TYPESOFOBSERV(self, line):

        if self.numberOfObservationTypes == 0:
            self.numberOfObservationTypes = int(line[0:6])

        typesLeft = self.numberOfObservationTypes - len(self.observationTypes)

        if typesLeft > 9:
            typesLeft = 9

        [self.observationTypes.append(line[(i+1)*6:(i+2)*6].strip()) for i in range(typesLeft)]

    def WAVELENGTHFACTL1_2(self, line):
        self.wavelengthFactor = np.array([int(line[0:6].strip()), int(line[6:12].strip())])

    def INTERVAL(self, line):
        self.interval = line[0:10]

    def TIMEOFFIRSTOBS(self, line):
        year = int(line[0:6])
        month = int(line[6:12])
        day = int(line[12:18])
        hour = int(line[18:24])
        min = int(line[24:30])
        sec = float(line[30:43])

        self.timeOfFristObs = np.array([year, month, day, hour, min, sec])
        self.timeSystem = line[48:51].strip()

    def TIMEOFLASTOBS(self, line):
        year = int(line[0:6])
        month = int(line[6:12])
        day = int(line[12:18])
        hour = int(line[18:24])
        min = int(line[24:30])
        sec = float(line[30:43])

        self.timeOfLastObs = np.array([year, month, day, hour, min, sec])
        #self.timeSystem = line[48:51].strip()



    def ENDOFHEADER(self, line):
        pass

    def getObservations(self, sat, obsType, opt=0):
        key = self.observationTypes.index(obsType)
        return np.append(self.observations[sat][:,0:6], self.observations[sat][:,6+key*3:6+key*3+1+2*opt], axis=1)





if __name__ == "__main__":

    reader = RNXReader("61300921A.19o")
    print(reader.timeOfFristObs)
    print(reader.timeSystem)
    print(reader.observationTypes)
    #print(reader.observations)
    print(np.shape(reader.getObservations('G08', "S1", 0)))
    print(reader.getObservations('G08', "S2", 0))
