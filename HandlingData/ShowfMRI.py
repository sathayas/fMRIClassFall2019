import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn.plotting import plot_epi, view_img
from nilearn.image import index_img

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'


# reading in the fMRI data array
f_fMRI = os.path.join(dataDir,'sub-26/func/sub-26_task-flanker_run-2_bold.nii.gz')
fMRI = nib.load(f_fMRI)
X_fMRI = fMRI.get_data()


# arbitrary voxel coordinate
xSlice = 32
ySlice = 28
zSlice = 22
tSlice = 0

# plotting the fMRI time series
plt.plot(np.arange(X_fMRI.shape[-1]), X_fMRI[xSlice,ySlice,zSlice,:],'co')
plt.xlabel('Time point')
plt.ylabel('Intensity')
plt.show()

# first extracting a time point from fMRI time series
single_image = index_img(X_fMRI, tSlice)

# showing the slngle image, extracted 3D volume from 4D data
plot_epi(single_image,
         display_mode='ortho',
         draw_cross=True,
         annotate=True,
         cmap='gray')

# interactive visualization
view_img(single_image, bg_img=False, cmap='gray', symmetric_cmap=False,
        vmin=50, vmax=1500, black_bg=True)
