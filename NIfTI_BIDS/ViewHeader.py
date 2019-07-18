import os
import numpy as np
import nibabel as nib


# Directory where your data set resides. 
dataDir = '/tmp/Data/ds102'

# reading in the fMRI data array
f_fMRI = os.path.join(dataDir,'sub-26/func/sub-26_task-flanker_run-2_bold.nii.gz')
fMRI = nib.load(f_fMRI)   # image object

# priting out the header information
hdr_fMRI = fMRI.header
print(hdr_fMRI)


# image dimension
print(hdr_fMRI.get_data_shape())

# data type
print(hdr_fMRI.get_data_dtype())

# voxel size
print(hdr_fMRI.get_zooms())
