import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn.plotting import plot_anat


# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# reading in the T1 image data array
f_sMRI = os.path.join(dataDir,'sub-26/anat/sub-26_T1w.nii.gz')
sMRI = nib.load(f_sMRI)
X_sMRI = sMRI.get_data()

# displaying image
plot_anat(f_sMRI,
          display_mode='ortho',
          dim=-1,
          draw_cross=True,
          annotate=True)

# average intensity in the x-direction
avgX_X_sMRI = X_sMRI.mean(axis=0)

# showing the resulting image
plt.imshow(np.rot90(avgX_X_sMRI), cmap='gray')
plt.axis('off')
