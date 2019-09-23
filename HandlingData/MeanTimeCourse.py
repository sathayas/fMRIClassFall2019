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


# plotting mean intensity over time
plt.plot(np.arange(nTime)+1, meanX_fMRI, 'b-')
plt.xlabel('Time points')
plt.ylabel('Average fMRI intensity (a.u.)')
plt.show()
