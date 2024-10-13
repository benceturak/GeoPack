import sys
sys.path.append('../../src')
sys.path.append('../../src/bernese_formats')
import epoch
import numpy as np
import matplotlib.pyplot as plt

def refractivityProfile(names,profiles, loc, fname, ep):
    font = {'size': 8}
    plt.rc('font', **font)
    fig, axs = plt.subplots(figsize=(3.31,3))
    plt.legend(prop = { "size": 8 })
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.rc('legend',fontsize=8)
    

    symbols = ['b--', 'r--', 'g-']

    for i in range(0, len(names)):
        name = names[i]
        profile = profiles[i]
        pcm = axs.plot(profile[:,1], profile[:,0], symbols[i], label=name)

        #axs.set(xlabel="Refractivity [-]", ylabel='Height [m]', fontsize=8)
        plt.xlabel("Refractivity [-]", fontsize=8)
        plt.ylabel('Height [m]', fontsize=8)
    plt.legend(fontsize=8)
    #plt.show()
    plt.savefig(fname, dpi=900, bbox_inches='tight')
    plt.close()
