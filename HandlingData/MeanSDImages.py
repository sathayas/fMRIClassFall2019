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

# calculating the mean and SD images
meanX_fMRI = X_fMRI.mean(axis=3)  # mean method with axis=3 (time)
stdX_fMRI = X_fMRI.std(axis=3)  # std method with axis=3 (time)


# arbitrary voxel coordinate for displaying
xSlice = 32
ySlice = 28
zSlice = 22

# displaying images, axial (xy-plane)
plt.imshow(np.rot90(meanX_fMRI[:,:,zSlice]), cmap='gray')
plt.title('Mean image')
plt.axis('off')
plt.show()

plt.imshow(np.rot90(stdX_fMRI[:,:,zSlice]), cmap='gray')
plt.title('SD image')
plt.axis('off')
plt.show()
