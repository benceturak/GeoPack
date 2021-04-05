import numpy as np
from normalformtofloat import normalFormToFloat
import math
from epoch import Epoch
from satellite import Satellite

class GPSNavReader(object):

    def __init__(self, fileName):

        self.fileName = fileName
        self.comments = []
        self.navigationDatas = {}
        try:
            self.fid = open(self.fileName, 'r')

            self._readHeader()
            self._readBody()

        finally:
            self.fid.close()

    def getSatellite(self, prn):

        sat = Satellite(prn)
        for i in self.navigationDatas[prn]:
            nav = {}
            nav['epoch'] = Epoch(i[0:6])

            nav['a0'] = i[6]
            nav['a1'] = i[7]
            nav['a2'] = i[8]

            nav['IODE'] = i[9]
            nav['Crs'] = i[10]
            nav['deltan'] = i[11]
            nav['M0'] = i[12]

            nav['Cuc'] = i[13]
            nav['e'] = i[14]
            nav['Cus'] = i[15]
            nav['a'] = i[16]**2

            nav['TOE'] = i[17]
            nav['Cic'] = i[18]
            nav['OMEGA'] = i[19]
            nav['Cis'] = i[20]

            nav['i0'] = i[21]
            nav['Crc'] = i[22]
            nav['omega'] = i[23]
            nav['OMEGADOT'] = i[24]

            nav['idot'] = i[25]
            nav['codesL2'] = i[26]
            nav['GPSWEEK'] = i[27]
            nav['flagL2P'] = i[28]

            nav['SVaccuracy'] = i[29]
            nav['SVhealth'] = i[30]
            nav['TGD'] = i[31]
            nav['IODC'] = i[32]

            nav['transmTime'] = i[33]
            nav['fitInterval'] = i[34]

            sat.addNavMess(nav)

        return sat



    def _readBody(self):
        line = self.fid.readline()


        while line:


            self._readEpochSatNav(line)
            line = self.fid.readline()

    def _readEpochSatNav(self, line):
        prn = "G" + line[0:2].replace(" ","0")



        if int(line[3:5]) > 80:
            year = 1900 + int(line[3:5])
        else:
            year = 2000 + int(line[3:5])

        month = int(line[6:8])
        day = int(line[9:11])
        hour = int(line[12:14])
        min = int(line[15:17])
        sec = float(line[17:22])



        clockBias = normalFormToFloat(line[22:41].strip())
        clockDrift = normalFormToFloat(line[41:60].strip())
        clockDriftRate = normalFormToFloat(line[60:79].strip())

        epoch = np.array([[year, month, day, hour, min, sec, clockBias, clockDrift, clockDriftRate]])

        for i in range(6):
            line = self.fid.readline()
            col1 = normalFormToFloat(line[3:22].strip())
            col2 = normalFormToFloat(line[22:41].strip())
            col3 = normalFormToFloat(line[41:60].strip())
            col4 = normalFormToFloat(line[60:79].strip())

            epoch = np.append(epoch, [[col1, col2, col3, col4]], axis=1)

        line = self.fid.readline()
        col1 = normalFormToFloat(line[3:22].strip())
        if line[22:41].strip() != '':
            col2 = normalFormToFloat(line[22:41].strip())
        epoch = np.append(epoch, [[col1, col2]], axis=1)


        if prn in self.navigationDatas.keys():
            self.navigationDatas[prn] = np.append(self.navigationDatas[prn], epoch, axis=0)
        else:
            self.navigationDatas[prn] = epoch


    def _readHeader(self):

        while True:

            line = self.fid.readline()

            type = line[60:].replace("/","_").replace(":","_").replace("-","_").replace("#","").replace(",","").replace(" ","").replace("\n","")


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

    reader = GPSNavReader("61300921A.19n")


    #print(reader.navigationDatas['G08'][0,0] == 2019)


    #print(reader.getValidEph('G08', Epoch(np.array([2019, 4, 2, 7, 48, 52]))))
    print(reader.getSatPos('G08', Epoch(np.array([2019, 4, 2, 7, 48, 52]))))
    #print(reader.beta)
    #print(reader.delta_utc)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
