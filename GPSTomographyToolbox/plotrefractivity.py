import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

def plotRefractivity(fname, ref, ep, cols=2):


    rows = int(np.shape(ref)[2]/cols)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    fig, axs = plt.subplots(rows, cols,figsize=(3.31,4), constrained_layout = True)
    pcm = np.empty((rows,cols))
    #plt.subplots_adjust(left=0.1, right=0.2, 
    #                top=0.9, bottom=0.0)
    for i in range(0,cols):
        for k in range(0,rows):
            pcm = axs[k,i].pcolormesh(ref[:,:,k*cols+i])
            axs[k,i].set_title(str(k*cols+i+1)+'. level ', fontsize=9)
            #axs[k,i].set_xticklabels(labels=[0,1,2,3,4,5,6,7],fontsize=8)
            #axs[k,i].set_yticklabels(labels=[0,1,2,3,4,5,6],fontsize=8)
            plt.sca(axs[k,i])
            plt.xticks(range(7),[15.5,17.0,18.5,20.0,21.5,23.0,24.5], fontsize=7, rotation=45)
            plt.yticks(range(6),[45.5,46.2,46.9,47.6,48.3,49.0], fontsize=7, rotation=45)
            cbar = fig.colorbar(pcm, ax=axs[k,i], orientation="vertical")
            #cbar.set_label("Rerfactivity [-]", fontsize=8)
            cbar.ax.tick_params(labelsize=8, rotation=90)
    #fig.suptitle("Refractivity ("+str(ep)+")")
    plt.savefig(fname, bbox_inches='tight')
    plt.close()
