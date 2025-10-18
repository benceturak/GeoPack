import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
import gc

matplotlib.use('Agg')

def plotOutliers(diffs, discarded, threshold, fname):


    fig, axs = plt.subplots(figsize=(3.31,3))


    print("____________________________")
    print(diffs)
    axs.plot(diffs[:,0]*180/np.pi, diffs[:,1], 'b.', markersize=3, label='SWD differences')
    if len(discarded[:,0]) > 0:
        axs.plot(discarded[:,0]*180/np.pi, discarded[:,1], 'r.', markersize=3, label='Discarded')

    axs.plot(threshold[:,0], threshold[:,1], 'g--', linewidth=1, label='Threshold')
    #axs.plot((b_min, b_max), (sig3_min_interval_min, sig3_min_interval_max), 'g--', linewidth=1, label='3sigma interval')

    plt.legend(fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
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




    #axs.axis([10, 90, 0, 0.5])
    plt.xlabel("Elevation angle [˚]", fontsize=8)
    plt.ylabel("SWD differences [m]", fontsize=8)

    #plt.show()
    plt.savefig(fname, dpi=900, bbox_inches='tight')
    fig.clf()
    plt.close()
    gc.collect()
