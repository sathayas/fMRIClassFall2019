import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'


# reading in the fMRI data array
f_fMRI = os.path.join(dataDir,'sub-26/func/sub-26_task-flanker_run-2_bold.nii.gz')
fMRI = nib.load(f_fMRI)
X_fMRI = fMRI.get_data()


# Mean intensity at each time points
nTime = X_fMRI.shape[-1]  # number of time points
meanX_fMRI = np.zeros(nTime)  # creating an array with nTime data points
for iTime in range(nTime):
    meanX_fMRI[iTime] = X_fMRI[:,:,:,iTime].mean()

# arbitrary voxel coordinate
xSlice = 32
ySlice = 28
zSlice = 22

# extracting voxel time course, then de-meaning
voxel_fMRI = X_fMRI[xSlice, ySlice, zSlice, :]
demean_fMRI = voxel_fMRI - meanX_fMRI[xSlice, ySlice, zSlice]


# plotting
plt.subplot(211)
plt.plot(np.arange(nTime)+1, voxel_fMRI, 'b-')
plt.xlabel('Time points')
plt.ylabel('Original fMRI (a.u.)')

plt.subplot(212)
plt.plot(np.arange(nTime)+1, demean_fMRI, 'b-')
plt.xlabel('Time points')
plt.ylabel('De-meaned fMRI (a.u.)')
plt.show()
