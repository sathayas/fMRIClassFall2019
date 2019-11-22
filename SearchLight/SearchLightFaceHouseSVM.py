import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.plotting import plot_roi
from nilearn.input_data import NiftiMasker
from sklearn.decomposition import PCA
from nilearn.image import new_img_like, load_img



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
imgMask = haxby_dataset.mask   # ventral-temporal streaming mask
tableTarget = haxby_dataset.session_target[0]  # session target table file




###### AREA TO FOCUS ON
voxXmin = 6
voxXmax = 34
voxYmin = 15
voxYmax = 30
voxZmin = 25
voxZmax = 33

# loading mask image
imgMask = load_img(haxby_dataset.mask)   # mask image object
X_mask = imgMask.get_data().astype(np.int)   # mask image array
X_box = np.zeros_like(X_mask)  # zero array, same size as X_mask

# Voxels within the box are turned to one
X_box[voxXmin:(voxXmax+1), voxYmin:(voxYmax+1), voxZmin:(voxZmax+1)] = 1

# creating a new image object for the box
imgBox = new_img_like(imgMask, X_box)

# Visualizing the mask, in relation to the anatomical
plot_roi(imgBox, bg_img=imgAnat, cmap='Paired')
plt.show()



###### LOADING AND MASKING IMAGE DATA

# Masking the image data with mask, extracting voxels
masker = NiftiMasker(mask_img=imgBox,
                     standardize=True,
                     detrend=True,
                     high_pass=0.008, t_r=TR)
# Extracting the voxel time series within the mask
X_fMRI = masker.fit_transform(imgfMRI)




###### LOADING BEHAVIORAL DATA
# loading the behavior data into a dataframe
targetData = pd.read_csv(tableTarget, sep=' ')
# stimulus types
targetNames = sorted(targetData.labels.unique())
# Creating numerical labels
targetData['labelInd'] = 0
for i,iCat in enumerate(targetNames):
    targetData.loc[targetData.labels==iCat, 'labelInd'] = i



###### MASKING FOR SELECTED STIMS
targetNames = ['face', 'house']  # the stims of interest
stimMask = targetData.labels.isin(targetNames)  # indices for the stim of interest
X_fMRI_selected = X_fMRI[stimMask]   # features (for selected stimuli only)
y = np.array(targetData.labelInd)[stimMask]  # labels
