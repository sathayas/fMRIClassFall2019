import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import nipype.interfaces.fsl as fsl # importing FSL interface functions
from nilearn.plotting import plot_anat, plot_epi, view_img


# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# an T1 weighted image from one of the subjects
imageT1 = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')
