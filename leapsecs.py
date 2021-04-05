import wget
import urllib
import numpy as np
import os

class LeapSecs(object):

    def __init__(self, fileName = 'Leap_Second.dat', url='https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat', download=False):
        self.fileName = fileName
        self.leapSecs = np.empty((0,5))

        try:
            if download:
                if os.path.exists(fileName):
                    os.remove(fileName)
                wget.download(url, fileName)
                print()
            self.fid = open(self.fileName, 'r')

            self._read()
        except urllib.error.HTTPError:
            print("Leapsec file connet be downloaded!")
        finally:
            self.fid.close()

    def _read(self):


        while True:
            line = self.fid.readline()
            if line[0:1] == "#":
                print(line)
            elif line[0:1] == " ":
                self.leapSecs = np.append(self.leapSecs, [[float(line[0:13].strip()), int(line[13:16].strip()), int(line[16:19].strip()), int(line[19:24].strip()), int(line[24:33].strip())]], axis=0)
            else:
                break




if __name__ == "__main__":
    ls = LeapSecs()

    print(ls.leapSecs)
