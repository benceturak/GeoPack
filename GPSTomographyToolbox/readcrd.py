import sys
sys.path.append('../')
import numpy as np
from station import Station
from network import Network
from ellipsoid import WGS84

class ReadCRD(object):
    """!ReadCRD class to read Bernese CRD format file The content of the Bernese CRD file will be sored and can be used inv the newtork parameter of the class in a Network object.
    """

    def __init__(self, fileName):
        """!ReadCRD constructor
        @param fileName (str): name of CRD file

        """

        #filename
        self.fileName = fileName
        #output Network object
        self.network = Network()

        #try to open and read CRD file
        try:
            #open CRD file
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
            #start read of stations
            self._readBody()
        finally:
            #close CRD file
            self.fid.close()

    def _readBody(self):
        """!read CRD body

        """
        #read next row
        line = self.fid.readline()

        #read stations row by row
        while line:
            #if line is empty, break the while cycle
            if line.strip() == '':
                break

            #read the cols
            #numerical Id of rows
            numId = line[0:3]
            #station ID
            digit4Id = line[5:9]
            #station dom ID
            dom = line[11:21]
            #station coordinates
            x = float(line[22:36])
            y = float(line[37:51])
            z = float(line[52:66])
            #station flag
            flag = line[68:]


            #create a new Station object with the coordinates
            st = Station(id=digit4Id, code=numId, coord=np.array([[x,y,z]]),system=WGS84())
            #add Station to the Network
            self.network.addStation(st)
            #read the next line
            line = self.fid.readline()

    def _readHeader(self):
        """!read CRD header

        """

        #read Bernese CRD file header row by row
        for i in range(0,6):

            line = self.fid.readline()#read row
            #print(line)
            continue

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

    reader = ReadCRD("../../example/BME001.CRD")

    print(reader.network.getStationsMatrix())


    #print(reader.beta)
    #print(np.shape(reader.getObservations('G08', "S1", 0)))
    #print(reader.getObservations('G08', "S2", 0))
