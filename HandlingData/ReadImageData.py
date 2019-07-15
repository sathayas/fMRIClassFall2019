import os
import numpy as np
import nibabel as nib

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# paths for the structural and functional MRI data.
f_sMRI = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')
f_fMRI = os.path.join(dataDir,'sub-26/func/sub-26_task-flanker_run-2_bold.nii.gz')

# reading in the image data arrays
# structural MRI
sMRI = nib.load(f_sMRI)
X_sMRI = sMRI.get_data()

# fMRI
fMRI = nib.load(f_fMRI)
X_fMRI = fMRI.get_data()
