import numpy as np
from normalformtofloat import normalFormToFloat
import math
from epoch import Epoch
from satellite import Satellite
import logging
from navreader import NavReader

class GalileoNavReader(NavReader):
    """
        GalileoNAvReader class to read RINEX navigation (Galileo) file
        RINEX v2.10

            :param fileName: name of navigation file (string)
    """


    def getSatellite(self, prn):

        sat = Satellite(prn)
        for i in self.navigationDatas[prn]:
            nav = {}
            nav['epoch'] = i[0]

            nav['a0'] = i[1]
            nav['a1'] = i[2]
            nav['a2'] = i[3]

            nav['IODE'] = i[4]
            nav['Crs'] = i[5]
            nav['deltan'] = i[6]
            nav['M0'] = i[7]

            nav['Cuc'] = i[8]
            nav['e'] = i[9]
            nav['Cus'] = i[10]
            nav['a'] = i[11]**2

            nav['TOE'] = i[12]
            nav['Cic'] = i[13]
            nav['OMEGA'] = i[14]
            nav['Cis'] = i[15]

            nav['i0'] = i[16]
            nav['Crc'] = i[17]
            nav['omega'] = i[18]
            nav['OMEGADOT'] = i[19]

            nav['idot'] = i[20]
            nav['codesL2'] = i[21]
            nav['GPSWEEK'] = i[22]
            nav['flagL2P'] = i[23]

            nav['SVaccuracy'] = i[24]
            nav['SVhealth'] = i[25]
            nav['TGD'] = i[26]
            nav['IODC'] = i[27]

            nav['transmTime'] = i[28]
            nav['fitInterval'] = i[29]

            sat.addNavMess(nav)

        return sat



    def _readBody(self):
        """read navigation messages

        """
        line = self.fid.readline()

        #read navigation datas row by row
        while line:

            #read satellite navigation datas in a valid epoch
            if self.version[0] == 2:
                self._readEpochSatNavV2(line)
            elif self.version[0] == 3:
                self._readEpochSatNavV3(line)

            line = self.fid.readline()

    def _readEpochSatNavV2(self, line):


        #read epoch
        prn = "G" + line[0:2].replace(" ","0")#satellite PRN extanded system markar and 0 if necessary


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


        #satellite clock error polynom coefficients
        clockBias = normalFormToFloat(line[22:41].strip())
        clockDrift = normalFormToFloat(line[41:60].strip())
        clockDriftRate = normalFormToFloat(line[60:79].strip())

        navDatas = np.array([[Epoch(np.array([year, month, day, hour, min, sec])), clockBias, clockDrift, clockDriftRate]])

        #read datas row by row
        for i in range(6):
            line = self.fid.readline()
            col1 = normalFormToFloat(line[3:22].strip())#cell 1
            col2 = normalFormToFloat(line[22:41].strip())#cell 2
            col3 = normalFormToFloat(line[41:60].strip())#cell 3
            col4 = normalFormToFloat(line[60:79].strip())#cell 4

            navDatas = np.append(navDatas, [[col1, col2, col3, col4]], axis=1)


        #read last residual row
        line = self.fid.readline()
        col1 = normalFormToFloat(line[3:22].strip())
        if line[22:41].strip() != '':
            col2 = normalFormToFloat(line[22:41].strip())
        navDatas = np.append(navDatas, [[col1, col2]], axis=1)


        if prn in self.navigationDatas.keys():#if already there is at least one observation to this satellite
            self.navigationDatas[prn] = np.append(self.navigationDatas[prn], navDatas, axis=0)
        else:#if there is not observation to this satellite
            self.navigationDatas[prn] = navDatas

    def _readEpochSatNavV3(self, line):


        #read epoch
        prn = line[0:3]#satellite PRN extanded system markar and 0 if necessary


        year = int(line[4:8])
        month = int(line[9:11])
        day = int(line[12:14])
        hour = int(line[15:17])
        min = int(line[18:20])
        sec = int(line[21:23])



        #satellite clock error polynom coefficients
        clockBias = normalFormToFloat(line[23:42].strip())
        clockDrift = normalFormToFloat(line[42:61].strip())
        clockDriftRate = normalFormToFloat(line[61:80].strip())

        navDatas = np.array([[Epoch(np.array([year, month, day, hour, min, sec])), clockBias, clockDrift, clockDriftRate]])

        #read datas row by row
        for i in range(6):
            line = self.fid.readline()
            col1 = normalFormToFloat(line[4:23].strip())#cell 1
            col2 = normalFormToFloat(line[23:42].strip())#cell 2
            col3 = normalFormToFloat(line[42:61].strip())#cell 3
            if line[61:80].strip() != '':
                col4 = normalFormToFloat(line[61:80].strip())#cell 4
            else:
                col4 = 0

            navDatas = np.append(navDatas, [[col1, col2, col3, col4]], axis=1)


        #read last residual row
        line = self.fid.readline()
        col1 = normalFormToFloat(line[4:23].strip())
        if line[23:42].strip() != '':
            col2 = normalFormToFloat(line[23:42].strip())
        navDatas = np.append(navDatas, [[col1, col2]], axis=1)


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

    def IONALPHA(self, line):
        a0 = normalFormToFloat(line[2:14].strip())
        a1 = normalFormToFloat(line[14:26].strip())
        a2 = normalFormToFloat(line[26:38].strip())
        a3 = normalFormToFloat(line[38:50].strip())

        self.alpha = np.array([a0, a1, a2, a3])

    def IONBETA(self, line):
        b0 = normalFormToFloat(line[2:14].strip())
        b1 = normalFormToFloat(line[14:26].strip())
        b2 = normalFormToFloat(line[26:38].strip())
        b3 = normalFormToFloat(line[38:50].strip())

        self.beta = np.array([b0, b1, b2, b3])

    def DELTA_UTC_A0A1TW(self,line):
        a0 = normalFormToFloat(line[3:22].strip())
        a1 = normalFormToFloat(line[22:41].strip())
        T = int(line[41:50])
        W = int(line[50:59])
        self.delta_utc = np.array([a0, a1, T, W])

    def ENDOFHEADER(self,line):
        pass
if __name__ == "__main__":

    reader = GalileoNavReader("../data/tomography/BRDC00WRD_R_20173640000_01D_EN.rnx")


    print(reader.navigationDatas['E08'])

    #print(reader.beta)
    #print(reader.delta_utc)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
