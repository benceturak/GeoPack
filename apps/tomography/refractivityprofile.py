import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import epoch
import numpy as np
import matplotlib.pyplot as plt

def refractivityProfile(names,profiles, loc, fname, ep):

    fig, axs = plt.subplots()

    symbols = ['b--', 'r-', 'g-']

    for i in range(0, len(names)):
        name = names[i]
        profile = profiles[i]
        pcm = axs.plot(profile[:,1], profile[:,0], symbols[i], label=name)

        axs.set(xlabel="Refractivity [-]", ylabel='height [m]', title='Refractivity '+loc+' ('+str(ep)+')')
    plt.legend()
    #plt.show()
    plt.savefig(fname)
    plt.close()
