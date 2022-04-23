

class NavReader(object):
    """NavReader class for general GNSS system

    """
    def __init__(self, fileName):
        """NavReader constructor

        """

        self.fileName = fileName#filename
        self.comments = []#comment records
        self.navigationDatas = {}#navigation datas
        try:
            self.fid = open(self.fileName, 'r')
            #start read of header
            self._readHeader()
            #start read of navigation datas
            self._readBody()

        finally:
            self.fid.close()

    def getSatellites(self):
        """Get all of satellites
            :return: satellites (Satellite) generator
        """
        for n in self.navigationDatas:
            yield self.getSatellite(n)
