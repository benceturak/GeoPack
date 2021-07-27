import numpy as np
import matplotlib.pyplot as plt

def plotRefractivity(ref, cols=2):


    rows = int(np.shape(ref)[0]/cols)

    fig, axs = plt.subplots(rows, cols)
    pcm = np.empty((rows,cols))
    for i in range(0,cols):
        for k in range(0,rows):
            pcm = axs[k,i].pcolormesh(ref[k*cols+i,:,:])
            axs[k,i].set(xlabel="lon", ylabel='lat', title=str(k*cols+i+1)+'. level ')
            fig.colorbar(pcm, ax=axs[k,i])
    plt.show()
