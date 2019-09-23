import os
import numpy as np
import nibabel as nib


# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# reading in the T1w data array
f_sMRI = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')
sMRI = nib.load(f_sMRI)   # image object

# the header information and priting pertinent information
hdr_sMRI = sMRI.header

# image dimension
print(hdr_sMRI.get_data_shape())

# data type
print(hdr_sMRI.get_data_dtype())

# voxel size
print(hdr_sMRI.get_zooms())
