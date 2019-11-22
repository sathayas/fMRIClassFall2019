import os
import numpy as np
import nibabel as nib

# AAL atlas
fAAL = '/tmp/Codes/Decoding/aal_MNI_V4.nii.gz'

# Sample fMRI data (pre-processed)
ffMRI = '/tmp/Data/ds114/derivatives_selected/fmriprep/sub-01/ses-test/func/'
ffMRI += 'sub-01_ses-test_task-fingerfootlips_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'

# Post-central gyrus
fPoCG = '/tmp/Codes/Decoding/aal_MNI_PoCG.nii.gz'
# Pre-central gyrus
fPreCG = '/tmp/Codes/Decoding/aal_MNI_PreCG.nii.gz'
# Pre and post central gyrus
fPrePoCG = '/tmp/Codes/Decoding/aal_MNI_PrePoCG.nii.gz'
# Binary mask image
fbPrePoCG = '/tmp/Codes/Decoding/aal_MNI_bPrePoCG.nii.gz'
# Resliced binary mask image
frbPrePoCG = '/tmp/Codes/Decoding/aal_MNI_rbPrePoCG.nii.gz'

# FSL maths commands for mask selecting the ROIs
com_PoCG = 'fslmaths ' + fAAL
com_PoCG += ' -thr 56.5 -uthr 58.5 ' + fPoCG
res = os.system(com_PoCG)

com_PreCG = 'fslmaths ' + fAAL
com_PreCG += ' -thr 0.5 -uthr 2.5 ' + fPreCG
res = os.system(com_PreCG)


# FSL maths command to combine the two masks
com_add = 'fslmaths ' + fPreCG
com_add += ' -add ' + fPoCG
com_add += ' ' + fPrePoCG
res = os.system(com_add)

# Converting to binary image
com_bin = 'fslmaths ' + fPrePoCG
com_bin += ' -bin ' + fbPrePoCG
res = os.system(com_bin)

# Reslicing the PrePoCG mask into the fMRI space
DirFSL = os.environ['FSLDIR']
feye = os.path.join(DirFSL, 'etc/flirtsch/ident.mat')

# actual reslicing using flirt functionality
com_flirt = 'flirt -in ' + fbPrePoCG
com_flirt += ' -applyxfm -init ' + feye
com_flirt += ' -out ' + frbPrePoCG
com_flirt += ' -paddingsize 0.0'
com_flirt += ' -interp nearestneighbour'
com_flirt += ' -ref ' + ffMRI
res = os.system(com_flirt)
