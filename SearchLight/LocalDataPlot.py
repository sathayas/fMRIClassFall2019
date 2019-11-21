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




###### NEIGHBORHOOD AROUND A VOXEL (WITHIN VT AREA)
voxX = 27
voxY = 23
voxZ = 30
boxWidth = 5
boxHalfWidth = np.floor(boxWidth/2).astype(int)  # half box width

# loading mask image
imgMask = load_img(haxby_dataset.mask)   # mask image object
X_mask = imgMask.get_data().astype(np.int)   # mask image array

# zero-ing voxels outside the box
X_mask[:(voxX-boxHalfWidth),:,:] = 0
X_mask[(voxX+boxHalfWidth+1):,:,:] = 0
X_mask[:,:(voxY-boxHalfWidth),:] = 0
X_mask[:,(voxY+boxHalfWidth+1):,:] = 0
X_mask[:,:,:(voxZ-boxHalfWidth)] = 0
X_mask[:,:,(voxZ+boxHalfWidth+1):] = 0

# creating a new image object for the box
imgBox = new_img_like(imgMask, X_mask)

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




##### PLOTTING DIMENSION REDUCED DATA
# PCA with largest 2 PCs
fMRIpca = PCA(n_components=2)
PC = fMRIpca.fit_transform(X_fMRI_selected)


# plotting the low dimension data (bottle, scissors and face only)
plt.figure(figsize=[9,9])
plt.scatter(PC[:,0], PC[:,1], c=y)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()






###### NEIGHBORHOOD AROUND A VOXEL (OUTSIDE VT AREA)
voxX = 30
voxY = 15
voxZ = 30

# loading mask image
imgMask = load_img(haxby_dataset.mask)   # mask image object
X_mask = imgMask.get_data().astype(np.int)   # mask image array

# zero-ing voxels outside the box
X_mask[:(voxX-boxHalfWidth),:,:] = 0
X_mask[(voxX+boxHalfWidth+1):,:,:] = 0
X_mask[:,:(voxY-boxHalfWidth),:] = 0
X_mask[:,(voxY+boxHalfWidth+1):,:] = 0
X_mask[:,:,:(voxZ-boxHalfWidth)] = 0
X_mask[:,:,(voxZ+boxHalfWidth+1):] = 0

# creating a new image object for the box
imgBox = new_img_like(imgMask, X_mask)

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
# masking for selected stims
X_fMRI_selected = X_fMRI[stimMask]   # features (for selected stimuli only)




##### PLOTTING DIMENSION REDUCED DATA
# PCA with largest 2 PCs
fMRIpca = PCA(n_components=2)
PC = fMRIpca.fit_transform(X_fMRI_selected)


# plotting the low dimension data (bottle, scissors and face only)
plt.figure(figsize=[9,9])
plt.scatter(PC[:,0], PC[:,1], c=y)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
