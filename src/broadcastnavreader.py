import numpy as np
import math
from epoch import Epoch
from satellite import Satellite
import logging
import gpsnavreader
import glonassnavreader
import galileonavreader

class BroadcastNavReader(gpsnavreader.GPSNavReader, glonassnavreader.GLONASSNavReader, galileonavreader.GalileoNavReader):
    """
        BroadcastNacReader class to read RINEX navigation (MIXED) file
        RINEX v3.03

            :param fileName: name of navigation file (string)
    """

    def getSatellite(self, prn):

        if prn[0] == 'G':
            return gpsnavreader.GPSNavReader.getSatellite(self,prn)
        elif prn[0] == 'R':
            return glonassnavreader.GLONASSNavReader.getSatellite(self,prn)
        elif prn[0] == 'E':
            return galileonavreader.GalileoNavReader.getSatellite(self,prn)
        elif prn[0] == 'C':
            pass
        else:
            pass


    def _readBody(self):
        """read navigation messages

        """
        line = self.fid.readline()

        #read navigation datas row by row
        while line:

            #read satellite navigation datas in a valid epoch
            if line[0] == 'G':
                gpsnavreader.GPSNavReader._readEpochSatNavV3(self,line)
            elif line[0] == 'R':
                glonassnavreader.GLONASSNavReader._readEpochSatNavV3(self,line)
            elif line[0] == 'E':
                galileonavreader.GalileoNavReader._readEpochSatNavV3(self,line)
            elif line[0] == 'C':
                pass
            else:
                pass

            line = self.fid.readline()


    def _readHeader(self):
        """read RINEX nav header v3.0

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

if __name__ == "__main__":

    reader = BroadcastNavReader("../data/tomography/BRDM00DLR_S_20211840000_01D_MN.rnx")

    sat = reader.getSatellite('E09')
    print(sat.getSatPos(Epoch(np.array([2021,7,3,12,12,45.14]))))

    #print(reader.beta)
    #print(reader.delta_utc)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
