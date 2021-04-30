import numpy as np
import math
import logging
from epoch import Epoch

class RNXReader(object):
    """
        RNXReader class to read RINEX observation file
        RINEX v2.10

            :param fileName: name of RINEX file (string)

    """

    def __init__(self, fileName):
        """RNXReader constructor

        """
        self.fileName = fileName#filname
        self.comments = []#comment records
        self.observationTypes = []#list of observation types
        self.numberOfObservationTypes = 0#number of observation types
        self.observations = {}#observations
        try:
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
        except IOError as e:
            #handle open file error
            logging.error(e)

    def getValidTimeFrame(self):
        pass

    def readObservations(self):
        """read observations from RINEX file

        """
        line = self.fid.readline()

        #read observation file row by row
        while line:
            #read next epoch
            self._readEpochSats(line)
            line = self.fid.readline()


    def _readEpochSats(self, line):
        """read satellites at epoch
                :param line: line from RINEX file (string)
        """

        listOfSats = []
        #read epoch
        #read 2 digits year and convert to 4 digits
        if int(line[1:3]) > 80:
            year = 1900 + int(line[1:3])
        else:
            year = 2000 + int(line[1:3])

        month = int(line[4:6])
        day = int(line[7:9])
        hour = int(line[10:12])
        min = int(line[13:15])
        sec = float(line[15:26])

        #epoch
        epoch = Epoch(np.array([year, month, day, hour, min, sec]))

        #epoch state flag
        epochFlag = int(line[28:29])

        #number of satellites in this epoch
        numOfSats = int(line[29:32])


        rows = int((numOfSats-1)/12)#number of full(12 satellites) rows
        resid = numOfSats%12#residual satellites in last row

        #if residual is 0, then the row is full
        if resid == 0:
            resid = 12

        #read the satellites whats are observed in this epoch
        for j in range(rows):#full rows
            [listOfSats.append(line[32+i*3:35+i*3].replace(" ", "0")) for i in range(12)]
            line = self.fid.readline()

        [listOfSats.append(line[32+i*3:35+i*3].replace(" ", "0")) for i in range(resid)]#residual

        #read observation sat by sat
        for i in range(numOfSats):
            sat = listOfSats[i]


            if sat in self.observations.keys():#if already there is at least one observation to this satellite
                self.observations[sat] = np.append(self.observations[sat], self._readObs(epoch), axis=0)
            else:#if there is not observation to this satellite
                self.observations[sat] = self._readObs(epoch)



    def _readObs(self, epoch):
        """read observations by satellites of epoch
                :epoch: epoch of observations(Epoch)
        """
        #return observation in epoch
        re_epoch = np.array([[epoch]])
        #number of full rows to one sat
        obsRows = int(self.numberOfObservationTypes / 5)
        #number of observations in the residual row
        obsResid = self.numberOfObservationTypes % 5

        #read observations row by row
        for i in range(obsRows):#full rows
            line = self.fid.readline()
            for j in range(5):#step on every observation blocks
                block = line[0+j*16:16+j*16]
                #observation
                if block[0:14].strip() == '':#if empty the vlue is 0
                    obs = 0
                else:
                    obs = float(block[0:14])
                #LLI
                if block[14:15].strip() == '':#if empty the vlue is 0
                    LLI = 0
                else:
                    LLI = int(block[14:15])
                #signal strength
                if block[15:16].strip() == '':#if empty the vlue is 0
                    sigStr = 0
                else:
                    sigStr = int(block[15:16])

                re_epoch = np.append(re_epoch, [[obs, LLI, sigStr]], axis=1)

        #residual row
        line = self.fid.readline()
        for j in range(obsResid):#step on every observation blocks
            block = line[0+j*16:16+j*16]

            #observation
            if block[0:14].strip() == '':#if empty the vlue is 0
                obs = 0
            else:
                obs = float(block[0:14])
            #LLI
            if block[14:15].strip() == '':#if empty the vlue is 0
                LLI = 0
            else:
                LLI = int(block[14:15])
            #signal strength
            if block[15:16].strip() == '':#if empty the vlue is 0
                sigStr = 0
            else:
                sigStr = int(block[15:16])

            re_epoch = np.append(re_epoch, [[obs, LLI, sigStr]], axis=1)

        return re_epoch



    def _readHeader(self):
        """read RINEX header v2.10

        """
        #read RINEX file row by row
        while True:

            line = self.fid.readline()#read a row

            type = line[60:].replace("/","_").replace(":","_").replace("#","").replace(" ","").replace("\n","")#replace special chars in title


            try:
                #read header record
                eval("self."+type+"(line)")
                logging.info(line[60:].strip() + " record is readed")
            except AttributeError as er:
                logging.warning(line[60:].strip() + " cannot be readed")

            #break loop when header is ended
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

        self.timeOfFristObs = Epoch(np.array([year, month, day, hour, min, sec]))
        self.timeSystem = line[48:51].strip()

    def TIMEOFLASTOBS(self, line):
        year = int(line[0:6])
        month = int(line[6:12])
        day = int(line[12:18])
        hour = int(line[18:24])
        min = int(line[24:30])
        sec = float(line[30:43])

        self.timeOfLastObs = Epoch(np.array([year, month, day, hour, min, sec]))
        #self.timeSystem = line[48:51].strip()



    def ENDOFHEADER(self, line):
        pass

    def getObservations(self, sats, obsTypes = None, minTime=None, maxTime=None, opt=0):
        """get observation by satellite PRN and observation type

                :sat: list of PRN 3-digits system-char [GPS: G,GLONASS: R, Galileo: E (RINEX standards)] and PRN extended with 0 if necessary (tuple)
                :obsType: list of observation type, marked as in RINEX standard (tuple), if None list all observed types, default None
                :minTime: start epoch of time frame (Epoch), if None there is no start of frame, default None
                :maxTime: end epoch of time frame (Epoch), if None there is no end of frame, default None
                :opt: observation optionally can be extended obs informations [LLI, signal strenth] (int 0 or 1), default:0

        """

        if obsTypes is None:
            obsTypes = self.observationTypes
        observations = {}

        if opt > 1:
            opt = 1
        elif opt < 0:
            opt = 0
        ot = ()
        for t in obsTypes:
            try:
                self.observationTypes.index(t)
                ot = ot + (t,)
            except ValueError:
                logging.warning('There are no '+ t +' observations')
                continue
        obsTypes = ot
        for s in sats:

            try:
                satObs = self.observations[s]



            except KeyError:
                logging.warning('There are no observations for PRN ' + s)
                continue
            observations[s] = np.empty((0,1+len(obsTypes)*(1 + opt*2)))
            for o in satObs:
                obsEpoch = o[0]

                if minTime is not None and maxTime is not None:
                    if obsEpoch < minTime or maxTime < obsEpoch:
                        continue
                elif minTime is None and maxTime is not None:
                    if maxTime < obsEpoch:
                        continue
                elif minTime is not None and maxTime is None:
                    if obsEpoch < minTime:
                        continue
                for t in obsTypes:

                    key = self.observationTypes.index(t)

                    obsEpoch = np.append(obsEpoch, o[1+key*3:1+key*3+1+2*opt])
                observations[s] = np.append(observations[s], [obsEpoch], axis=0)





        #key of observation type


        return observations#np.append(self.observations[sat][:,0:1], self.observations[sat][:,1+key*3:1+key*3+1+2*opt], axis=1)





if __name__ == "__main__":

    reader = RNXReader("61300921A.19o")
    print(reader.timeOfFristObs)
    print(reader.timeSystem)
    print(reader.observationTypes)
    #print(reader.observations)
    print(np.shape(reader.getObservations('G08', "S1", 0)))
    print(reader.getObservations('G08', "S2", 0))
