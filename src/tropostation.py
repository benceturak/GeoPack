import numpy as np

def NeillFormula(e, a, b, c):
    return (1 + (a/(1 + b/(1 + c))))/(np.sin(e) + (a/(np.sin(e) + b/(np.sin(e) + c))))







class TropoStation(object):

    def __init__(self):
        pass


    def setTropoFromTRP(self, tropo):
        self.tropo = tropo

class VMF1(TropoStation):
    a_ht = 2.53*10**-5
    b_ht = 5.49*10**-3
    c_ht = 1.14*10**-3
    b_h = 0.0029
    b_w = 0.00146
    c0 = 0.062
    c10 = np.array([0.002, 0.001])
    c11 = np.array([0.007, 0.005])
    c_w = 0.04391
    PSZI = np.array([np.pi, 0])

    def __init__(self, vmf11grid):
        super(VMF1, self).__init__()

        self.vmf11grid = vmf1grid

    def heightCorrection(self, e):

        return 1/np.sin(e) - NeillFormula(e, self.a_ht, self.b_ht, self.c_h)



    def c_h(self, st, ep):
        doy = ep.MJD - 44239 + 1 - 28


        phi = st.getPLH()

        #norther hemisphere
        if phi[0] >= 0:
            i = 0
        #souther hemisphere
        else:
            i = 1

        c0 = self.c0
        PSZI = self.PSZI[i]
        c10 = self.c10[i]
        c11 = self.c11[i]

        return c0 + ((np.cos(doy/365*2*np.pi + PSZI) + 1)*c11/2 + c10)*(1 - cos(phi))

    def slantDelay_h(self, st, alpha, e, ep):

        a_h = self.vmf1grid.getA_h(st)


        NeillFormula(e, a_h, self.b, self.c_h(st, ep))
