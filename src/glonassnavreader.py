import numpy as np
from normalformtofloat import normalFormToFloat
import math
import epoch
from satellite import Satellite
import logging

class GLONASSNavReader(object):
    """
        GPSNAvReader class to read RINEX navigation (GPS) file
        RINEX v2.10

            :param fileName: name of navigation file (string)
    """

    def __init__(self, fileName):
        """GPSNavReader condtructor

        """

        self.fileName = fileName#filename
        self.comments = []#comment records
        self.navigationDatas = {}#navigation datas
        self.tauC = epoch.Epoch(np.array([0, 0, 0, 0, 0, 0]))
        try:
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
            #start read of navigation datas
            self._readBody()
        finally:
            self.fid.close()

    def getSatellite(self, prn):

        sat = Satellite(prn)
        for i in self.navigationDatas[prn]:
            nav = {}
            nav['epoch'] = i[0]

            nav['tauC'] = self.tauC


            nav['tauN'] = i[1]
            nav['gammaN'] = i[2]
            nav['tk'] = i[3]

            nav['x0'] = i[4]*1000
            nav['dxdt'] = i[5]*1000
            nav['dxdt2'] = i[6]*1000
            nav['health'] = i[7]

            nav['y0'] = i[8]*1000
            nav['dydt'] = i[9]*1000
            nav['dydt2'] = i[10]*1000
            nav['freqNum'] = i[11]**2

            nav['z0'] = i[12]*1000
            nav['dzdt'] = i[13]*1000
            nav['dzdt2'] = i[14]*1000
            nav['operInfo'] = i[15]

            sat.addNavMess(nav)

        return sat



    def _readBody(self):
        """read navigation messages

        """
        line = self.fid.readline()

        #read navigation datas row by row
        while line:

            #read satellite navigation datas in a valid epoch
            self._readEpochSatNav(line)
            line = self.fid.readline()

    def _readEpochSatNav(self, line):


        #read epoch
        prn = "R" + line[0:2].replace(" ","0")#satellite PRN extanded system markar and 0 if necessary


        #read 2 digits year and convert to 4 digits
        if int(line[3:5]) > 80:
            year = 1900 + int(line[3:5])
        else:
            year = 2000 + int(line[3:5])

        month = int(line[6:8])
        day = int(line[9:11])
        hour = int(line[12:14])
        min = int(line[15:17])
        sec = float(line[17:22])


        #satellite clock error polynom coefrficients
        clockBias = normalFormToFloat(line[22:41].strip())
        relFreqBias = normalFormToFloat(line[41:60].strip())
        frameTime = normalFormToFloat(line[60:79].strip())

        navDatas = np.array([[epoch.Epoch(np.array([year, month, day, hour, min, sec]), system=epoch.UTC), clockBias, relFreqBias, frameTime]])

        #read datas row by row
        for i in range(3):
            line = self.fid.readline()
            col1 = normalFormToFloat(line[3:22].strip())#cell 1
            col2 = normalFormToFloat(line[22:41].strip())#cell 2
            col3 = normalFormToFloat(line[41:60].strip())#cell 3
            col4 = normalFormToFloat(line[60:79].strip())#cell 4

            navDatas = np.append(navDatas, [[col1, col2, col3, col4]], axis=1)


        if prn in self.navigationDatas.keys():#if already there is at least one observation to this satellite
            self.navigationDatas[prn] = np.append(self.navigationDatas[prn], navDatas, axis=0)
        else:#if there is not observation to this satellite
            self.navigationDatas[prn] = navDatas


    def _readHeader(self):
        """read RINEX nav header v2.0

        """

        #read navigation file row by row
        while True:

            line = self.fid.readline()#read row

            type = line[60:].replace("/","_").replace(":","_").replace("-","_").replace("#","").replace(",","").replace(" ","").replace("\n","")#replace special chars in title


            try:
                #read header record
                eval("self."+type+"(line)")
                logging.info(line[60:].strip() + " record is readed")
            except AttributeError as er:
                logging.warning(line[60:].strip() + " cannot be readed")

            if type == 'ENDOFHEADER':
                break

    def RINEXVERSION_TYPE(self, line):
        version = line[0:9].replace(" ","").split(".")

        version_1 = int(version[0])
        version_2 = int(version[1])

        self.version = np.array([version_1, version_2])
        self.fileType = line[20:21].replace(" ","")

    def PGM_RUNBY_DATE(self, line):
        self.programName = line[0:20].strip()
        self.agencyName = line[20:40].strip()
        self.date = line[40:60].strip()

    def COMMENT(self,line):
        self.comments.append(line[0:60].strip())

    def CORRTOSYSTEMTIME(self,line):

        self.reference = epoch.Epoch(np.array([int(line[0:6].strip()), int(line[6:12].strip()), int(line[12:18].strip()), 0, 0, 0]))
        self.tauC = epoch.Epoch(np.array([0, 0, 0, 0, 0, float(line[21:40].strip())]))


    def ENDOFHEADER(self,line):
        pass
if __name__ == "__main__":

    reader = GLONASSNavReader("../example/61300921A.19g")


    print(reader.navigationDatas['R08'])

    #print(reader.beta)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
