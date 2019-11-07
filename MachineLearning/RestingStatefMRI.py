import os
import matplotlib.pyplot as plt
import numpy as np

##### Parameters
targetDeg = 20

##### Loading the data
infile = np.load(os.path.join('DataML',
                              'Leiden_sub39335_Rt2_K200_Rmat.npz'))
Rmat = infile['Rmat']
nodes = infile['nodes']
xyz = infile['xyz']


##### Examples of correlation matrices
indTime = 0
plt.imshow(Rmat[indTime,:,:], cmap=plt.cm.rainbow)
plt.title('Correlation matrix, t=%-3d' % indTime)
plt.xlabel('Nodes')
plt.ylabel('Nodes')
plt.colorbar()

plt.show()


##### loading the efficiency metrics that have been pre-calculated
f = np.load(os.path.join('DataML',
                         'Leiden_sub39335_Rt2_K200_Efficiency.npz'))
ElocMat = f['ElocMat']
EglobMat = f['EglobMat']


##### plotting efficiency over time
plt.figure(figsize=[9,5])
plt.subplot(121)
plt.imshow(ElocMat, cmap=plt.cm.rainbow)
plt.title('Local efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.subplot(122)
plt.imshow(EglobMat, cmap=plt.cm.rainbow)
plt.title('Global efficiency')
plt.xlabel('Time')
plt.ylabel('Nodes')
plt.colorbar()

plt.show()
