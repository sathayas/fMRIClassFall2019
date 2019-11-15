import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker


##### PARAMETERS
TR = 2.5

##### DIRECTORY BUSINESS ######
# original data directory where haxby2001 directory resides
dataDir = '/tmp/Data'


##### DATA FILES
# By default 2nd subject will be fetched
haxby_dataset = datasets.fetch_haxby(data_dir=dataDir)
imgfMRI = haxby_dataset.func[0]   # fMRI data file
imgAnat = haxby_dataset.anat[0]   # structural data file
imgMaskVT = haxby_dataset.mask_vt[0]   # ventral-temporal streaming mask
tableTarget = haxby_dataset.session_target[0]  # session target table file



###### EXTRACTING DATA FROM ROI MASK

# Masking the image data with the VT mask, extracting voxels
masker = NiftiMasker(mask_img=imgMaskVT,
                     standardize=True,
                     detrend=True,
                     high_pass=0.008, t_r=TR)
# Extracting the voxel time series within the mask
X_fMRI = masker.fit_transform(imgfMRI)



##### BEHAVIORAL DATA
# loading the behavior data into a dataframe
targetData = pd.read_csv(tableTarget, sep=' ')
# stimulus types
targetNames = sorted(targetData.labels.unique())
# Creating numerical labels
targetData['labelInd'] = 0
for i,iCat in enumerate(targetNames):
    targetData.loc[targetData.labels==iCat, 'labelInd'] = i



##### SELECTED STIMULI ONLY
stimMask = targetData.labels.isin(['bottle', 'scissors', 'face'])
X = X_fMRI[stimMask]   # features (for selected stimuli only)
y = np.array(targetData.labelInd)[stimMask]
