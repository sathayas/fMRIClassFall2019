import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.plotting import plot_roi
from nilearn.input_data import NiftiMasker

##### PARAMETERS
TR = 2.5

##### DIRECTORY BUSINESS ######
# original data directory where haxby2001 directory resides
dataDir = '/tmp/Data'


# By default 2nd subject will be fetched
haxby_dataset = datasets.fetch_haxby(data_dir=dataDir)
imgfMRI = haxby_dataset.func[0]   # fMRI data file
imgAnat = haxby_dataset.anat[0]   # structural data file
imgMaskVT = haxby_dataset.mask_vt[0]   # ventral-temporal streaming mask

# Visualizing the mask, in relation to the anatomical
plot_roi(imgMaskVT, bg_img=imgAnat, cmap='Paired')

# Masking the image data with the VT mask, extracting voxels
masker = NiftiMasker(mask_img=imgMaskVT,
                     standardize=True,
                     detrend=True,
                     high_pass=0.008, t_r=TR)
# Extracting the voxel time series within the mask
X_fMRI = masker.fit_transform(imgfMRI)


# Plotting the data
voxID = 500
plt.plot(X_fMRI[voxID,:])
plt.xlabel('Time points (TR)')
plt.ylabel('BOLD signal (standardized)')
plt.show()
