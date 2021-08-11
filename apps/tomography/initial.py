import numpy as np

source_dir = '../../data/tomography/2021/'
x0 = np.array([51.32, 32.0, 20.0, 13.5, 6.6281, 0.2337])

x0_3D = np.empty((6,7,6))

x0_3D[:,:,0] = x0[0]
x0_3D[:,:,1] = x0[1]
x0_3D[:,:,2] = x0[2]
x0_3D[:,:,3] = x0[3]
x0_3D[:,:,4] = x0[4]
x0_3D[:,:,5] = x0[5]

np.save(source_dir+'initial.npy', x0_3D)
