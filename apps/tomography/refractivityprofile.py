import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import epoch
import numpy as np
import matplotlib.pyplot as plt

def refractivityProfile(names,profiles):

    fig, axs = plt.subplots()

    for i in range(0, len(names)):
        name = names[i]
        profile = profiles[i]

        pcm = axs.plot(profile[:,1], profile[:,0], label=name)

        axs.set(xlabel="Refractivity [-]", ylabel='height [m]', title='Refractivity Budapest')
    plt.legend()
    plt.show()
    #plt.savefig(fname)
