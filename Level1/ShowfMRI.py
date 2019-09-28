import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform

# Directory and file business
dataDir = '/tmp/Data/ds114'  # Data directory
anatDir = os.path.join(dataDir,'derivatives_selected/fmriprep/sub-09/anat/')
imageT1 = os.path.join(anatDir,
                       'sub-09_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')
featDir = os.path.join(dataDir,
                       'WorkflowOutput/feat_dir/run0.feat/')
statDir = os.path.join(featDir,'stats')
imageStat = os.path.join(statDir, 'tstat6.nii.gz')

# thresholding the stat image to positive values only for visualization
thImageStat = math_img("np.ma.masked_less(img, 0)",
                                     img=imageStat)

# stat map at the maximum
plot_stat_map(thImageStat, bg_img=imageT1,
              colorbar=True, threshold=2.3, black_bg=True,
              draw_cross=True,
              cut_coords=coord_transform(23,27,36,thImageStat.affine))


# interactive visualization
view_img(thImageStat, bg_img=imageT1, cmap='black_red',
         symmetric_cmap=False, annotate=True,
         colorbar=True, threshold=2.3, black_bg=True)
