import numpy as np
from normalformtofloat import normalFormToFloat
import math
from epoch import Epoch

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

    def getValidEph(self, prn, epoch):

        #frame = np.append([epoch - np.array([0, 0, 0, 1, 0, 0])], [epoch + np.array([0, 0, 0, 1, 0, 0])], axis=0)
        min = epoch - Epoch(np.array([0, 0, 0, 1, 0, 0]))
        max = epoch + Epoch(np.array([0, 0, 0, 1, 0, 0]))
        #frame = normalizeTime(frame)

        for nav in self.navigationDatas[prn]:
            ephEpoch = Epoch(nav[0:6])
            if min <= ephEpoch and ephEpoch <= max:

                ephemerids = {}

                ephemerids['epoch'] = nav[0:6]

                ephemerids['a0'] = nav[6]
                ephemerids['a1'] = nav[7]
                ephemerids['a2'] = nav[8]

                ephemerids['IODE'] = nav[9]
                ephemerids['Crs'] = nav[10]
                ephemerids['deltan'] = nav[11]
                ephemerids['M0'] = nav[12]

                ephemerids['Cuc'] = nav[13]
                ephemerids['e'] = nav[14]
                ephemerids['Cus'] = nav[15]
                ephemerids['a'] = nav[16]**2

                ephemerids['TOE'] = nav[17]
                ephemerids['Cic'] = nav[18]
                ephemerids['OMEGA'] = nav[19]
                ephemerids['Cis'] = nav[20]

                ephemerids['i0'] = nav[21]
                ephemerids['Crc'] = nav[22]
                ephemerids['omega'] = nav[23]
                ephemerids['OMEGADOT'] = nav[24]

                ephemerids['idot'] = nav[25]
                ephemerids['codesL2'] = nav[26]
                ephemerids['GPSWEEK'] = nav[27]
                ephemerids['flagL2P'] = nav[28]

                ephemerids['SVaccuracy'] = nav[29]
                ephemerids['SVhealth'] = nav[30]
                ephemerids['TGD'] = nav[31]
                ephemerids['IODC'] = nav[32]

                ephemerids['transmTime'] = nav[33]
                ephemerids['fitInterval'] = nav[34]

                return ephemerids
                break

    def getSatPos(self, prn, epoch):

        ephemerids = self.getValidEph(prn, epoch)


        t_temp = ephemerids['TOE']

        DOW = 0

        while t_temp >= 86400:
            t_temp -= 86400
            DOW += 1



        t = DOW*86400 + epoch.getUTC[3]*3600 + epoch.getUTC[4]*60 + epoch.getUTC[5]

        GM = 3.986005*10**14
        omegaE = 7.2921151467*10**(-5)

        tk = t - ephemerids['TOE']

        n0 = math.sqrt(GM/ephemerids['a']**3)
        n = n0 + ephemerids['deltan']
        Mk = ephemerids['M0'] + n*tk

        Ek = Mk

        d = 1
        while d > 10**(-12):
            E_l = Ek
            Ek = Mk + ephemerids['e']*math.sin(Ek)
            d = abs(Ek - E_l)

        nu = 2*math.atan(math.sqrt(1 + ephemerids['e'])/math.sqrt(1 - ephemerids['e'])*math.tan(Ek/2))

        phik = nu + ephemerids['omega']

        duk = ephemerids['Cuc']*math.cos(2*phik) + ephemerids['Cus']*math.sin(2*phik)
        drk = ephemerids['Crc']*math.cos(2*phik) + ephemerids['Crs']*math.sin(2*phik)
        dik = ephemerids['Cic']*math.cos(2*phik) + ephemerids['Cis']*math.sin(2*phik)

        uk = phik + duk
        rk = ephemerids['a']*(1 - ephemerids['e']*math.cos(Ek))+ drk
        ik = ephemerids['i0'] + ephemerids['idot']*tk + dik

        xk = rk*math.cos(uk)
        yk = rk*math.sin(uk)
        zk = 0

        coordsOrbPlane = np.array([[xk], [yk], [zk]])

        OMEGAk = ephemerids['OMEGA'] + (ephemerids['OMEGADOT'] - omegaE)*tk - omegaE*ephemerids['TOE']

        ROMEGA = np.array([[math.cos(OMEGAk), -math.sin(OMEGAk), 0], [-math.sin(OMEGAk), math.cos(OMEGAk), 0], [0, 0, 1]])
        Ri = np.array([[1, 0, 0], [0, math.cos(ik), -math.sin(ik)], [0, math.sin(ik), math.cos(ik)]])


        coords = np.dot(np.dot(ROMEGA, Ri), coordsOrbPlane)

        return coords





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
