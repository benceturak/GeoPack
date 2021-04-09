import wget
import urllib
import numpy as np
import os
from epoch import Epoch
import logging
class LeapSecs(object):
    """
        LeapSecs class to handle leap seconds
            :param fileName: (string), default Leap_second.dat
            :param url: url of leapsec file (string), default https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat (IERS bulletin C)
            :param download: download the leapsec file? (boolean), default False
    """

    def __init__(self, fileName = 'Leap_Second.dat', url='https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat', download=False):
        """LeapSecs construcor

        """
        self.fileName = fileName
        self.leapSecs = np.empty((0,3))

        try:
            if download:#download leap seconds file if necessary
                if os.path.exists(fileName):
                    os.remove(fileName)
                wget.download(url, fileName)
                print()
            self.fid = open(self.fileName, 'r')

            self._read()
        except urllib.error.HTTPError:
            logging.error("Leapsec file connet be downloaded!")
        finally:
            self.fid.close()

    def _read(self):
        """read leapsec file

        """

        #read leeapsec file row by row
        while True:
            line = self.fid.readline()
            if line[0:1] == "#":#header rows
                pass#print(line)
            elif line[0:1] == " ":#content
                self.leapSecs = np.append(self.leapSecs, [[float(line[0:13].strip()), Epoch(np.array([int(line[19:24].strip()), int(line[16:19].strip()), int(line[13-16].strip()),0,0,0])), int(line[24:33].strip())]], axis=0)
            else:
                break




if __name__ == "__main__":
    ls = LeapSecs()

    print(ls.leapSecs)
