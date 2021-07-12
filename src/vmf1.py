import numpy as np

def NeillFormula(e, a, b, c):
    return (1 + (a/(1 + b/(1 + c))))/(np.sin(e) + (a/(np.sin(e) + b/(np.sin(e) + c))))




class VMF1(object):
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

    def __init__(self, vmf1grid):
        super(VMF1, self).__init__()

        self.vmf1grid = vmf1grid

    def heightCorrection(self, e):

        return 1/np.sin(e) - NeillFormula(e, self.a_ht, self.b_ht, self.c_ht)



    def c_h(self, st, ep):
        doy = ep.MJD - 44239 + 1 - 28


        phi = st.getPLH()[0,0]

        #norther hemisphere
        if phi >= 0:
            i = 0
        #souther hemisphere
        else:
            i = 1

        c0 = self.c0
        PSZI = self.PSZI[i]
        c10 = self.c10[i]
        c11 = self.c11[i]

        return c0 + ((np.cos(doy/365*2*np.pi + PSZI) + 1)*c11/2 + c10)*(1 - np.cos(phi))

    def fun_h(self, st, e, ep):

        a_h = self.vmf1grid.getA_h(st)
        b_h = self.b_h
        c_h = self.c_h(st, ep)
        sine = np.sin(e)
        cose = np.cos(e)
        beta = b_h/(sine + c_h)
        gamma = a_h/(sine + beta)
        topcon = 1 + a_h/(1 + b_h/(1 + c_h))

        ht = st.getPLH()[2,0]/1000

        return topcon/(sine + gamma)

    def fun_h_der(self, st, e, ep):


        a_h = self.vmf1grid.getA_h(st)
        b_h = self.b_h
        c_h = self.c_h(st, ep)
        sine = np.sin(e)
        cose = np.cos(e)
        beta = b_h/(sine + c_h)
        gamma = a_h/(sine + beta)
        topcon = 1 + a_h/(1 + b_h/(1 + c_h))

        ht = st.getPLH()[2,0]/1000
        der = self.fun_h(st, e, ep)**2/topcon*cose*(1 - gamma**2/a_h*(1 - beta**2/b_h))
        #der = self.fun_h(st, e, ep)**2/(1 + (a_h/(1 + self.b_h/(1 + self.c_h(st, ep)))))*np.cos(e)*(1 - (a_h/(np.sin(e) + self.b_h/(np.sin(e) + self.c_h(st, ep))))**2/a_h*(1 - self.b_h/(np.sin(e) + self.c_h(st, ep))))
        a_h = self.a_ht
        b_h = self.b_ht
        c_h = self.c_ht
        sine = np.sin(e)
        cose = np.cos(e)
        beta = b_h/(sine + c_h)
        gamma = a_h/(sine + beta)
        topcon = 1 + a_h/(1 + b_h/(1 + c_h))


        return der + (cose/sine**2 - topcon*cose/(sine + gamma)**2*(1 - gamma**2/a_h*(1 - beta**2/b_h)))*ht
        #return der + (np.cos(e)/np.sin(e)**2 - (1 + (self.a_ht/(1 + self.b_ht/(1 + self.c_ht))))*np.cos(e)/(np.sin(e) + (self.a_ht/(np.sin(e) + self.b_ht/(np.sin(e) + self.c_ht))))**2*(1 - (self.a_ht/(np.sin(e) + self.b_ht/(np.sin(e) + self.c_ht)))**2/self.a_ht*(1 - (self.b_ht/(np.sin(e) + self.c_ht))**2/self.b_ht)))*ht


    def fun_w(self, st, e, ep):

        a_w = self.vmf1grid.getA_w(st)
        b_w = self.b_w
        c_w = self.c_w
        sine = np.sin(e)
        cose = np.cos(e)
        beta = b_w/(sine + c_w)
        gamma = a_w/(sine + beta)
        topcon = 1 + a_w/(1 + b_w/(1 + c_w))

        ht = st.getPLH()[2,0]/1000

        return topcon/(sine + gamma)

    def fun_w_der(self, st, e, ep):


        a_w = self.vmf1grid.getA_w(st)
        b_w = self.b_w
        c_w = self.c_w
        sine = np.sin(e)
        cose = np.cos(e)
        beta = b_w/(sine + c_w)
        gamma = a_w/(sine + beta)
        topcon = 1 + a_w/(1 + b_w/(1 + c_w))

        ht = st.getPLH()[2,0]/1000
        der = self.fun_w(st, e, ep)**2/topcon*cose*(1 - gamma**2/a_w*(1 - beta**2/b_w))

        return der
    def slantDelay_h(self, zd, st, alpha, e, grad_n, grad_e, ep):

        return self.fun_h(st, e, ep)*zd + grad_n*self.fun_h_der(st, e, ep)*np.cos(alpha) + grad_e*self.fun_h_der(st, e, ep)*np.sin(alpha)

    def slantDelay_w(self, zd, st, alpha, e, grad_n, grad_e, ep):

        return self.fun_w(st, e, ep)*zd + zd*grad_n*self.fun_w_der(st, e, ep)*np.cos(alpha) + zd*grad_e*self.fun_w_der(st, e, ep)*np.sin(alpha)
