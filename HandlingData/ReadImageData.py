import os
import numpy as np
import nibabel as nib

# Directory where your data set resides. This needs to be customized
dataDir = '/home/satoru/Teaching/fMRI_Fall_2018/Data/ds102'

# paths for the structural and functional MRI data. 
# NOTE that the paths are different for each user. You need to customize
f_sMRI = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')
f_fMRI = os.path.join(dataDir,'sub-26/func/sub-26_task-flanker_run-2_bold.nii.gz')

# reading in the image data arrays
# structural MRI
sMRI = nib.load(f_sMRI)
X_sMRI = sMRI.get_data()

# fMRI
fMRI = nib.load(f_fMRI)
X_fMRI = fMRI.get_data()


