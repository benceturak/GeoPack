import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def plotRegression(A, Nw_est, b, stas, fname, title):

    b = b *10**-6
    b_est = np.dot(A, Nw_est)*10**-6

    m, c, r, p, se = stats.linregress(b, b_est)
    fig, axs = plt.subplots()

    b_min = np.min(b)
    b_max = np.max(b)
    Y_min = m*b_min+c
    Y_max = m*b_max+c
    sig3_max_interval_min = (m+3*se)*b_min + c
    sig3_max_interval_max = (m+3*se)*b_max + c
    sig3_min_interval_min = (m-3*se)*b_min + c
    sig3_min_interval_max = (m-3*se)*b_max + c


    equation = "Y = {0:.4f}*x + {1:.4f}" .format(m, c)
    b_t = []
    b_est_t = []


    axs.plot(b, b_est, 'b*', label='Data')
    axs.plot((b_min, b_max), (Y_min, Y_max), 'r-', label='Fit')
    axs.plot((b_min, b_max), (b_min, b_max), 'k--', linewidth=1, label='input = estimated')
    axs.plot((b_max, b_min, b_max), (sig3_max_interval_max, sig3_min_interval_min, sig3_min_interval_max), 'g--', linewidth=2, label='3sigma interval')


    plt.legend()
    #for i in range(0,len(stas)):


        #if i == 0:
        #    b_t.append(b[i])
        #    b_est_t.append(b_est[i])
        #elif stas[i] == stas[i-1]:
        #    b_t.append(b[i])
        #    b_est_t.append(b_est[i])
        #else:
        #    m, c, r, p, se = stats.linregress(b_t, b_est_t)
        #    print(stas[i-1] + '|' + "Y = {0:.4f}*x + {1:.4f}" .format(m, c))
        #    axs.plot(b_t, b_est_t, '*', label=stas[i-1])
        #    b_t = []
        #    b_est_t = []




    axs.axis([b_min, b_max, b_min, b_max])

    axs.set(xlabel="ZWD [m]", ylabel=equation, title=title + ' R = {0:.5f}'.format(r))

    #plt.show()
    plt.savefig(fname)
    plt.close()
