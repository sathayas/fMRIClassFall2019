import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.plotting import plot_roi
from nilearn.input_data import NiftiMasker
from sklearn.decomposition import PCA



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

# Visualizing the mask, in relation to the anatomical
plot_roi(imgMaskVT, bg_img=imgAnat, cmap='Paired')


###### EXTRACTING DATA FROM ROI MASK

# Masking the image data with the VT mask, extracting voxels
masker = NiftiMasker(mask_img=imgMaskVT,
                     standardize=True,
                     detrend=True,
                     high_pass=0.008, t_r=TR)
# Extracting the voxel time series within the mask
X_fMRI = masker.fit_transform(imgfMRI)


# Plotting the data
voxID = 500
plt.plot(X_fMRI[voxID,:])
plt.xlabel('Time points (TR)')
plt.ylabel('BOLD signal (standardized)')
plt.show()



##### BEHAVIORAL DATA
# loading the behavior data into a dataframe
targetData = pd.read_csv(tableTarget, sep=' ')
# stimulus types
targetNames = sorted(targetData.labels.unique())
# Creating numerical labels
targetData['labelInd'] = 0
for i,iCat in enumerate(targetNames):
    targetData.loc[targetData.labels==iCat, 'labelInd'] = i




##### PLOTTING DIMENSION REDUCED DATA
# PCA with largest 2 PCs
fMRIpca = PCA(n_components=2)
PC = fMRIpca.fit_transform(X_fMRI)

# plotting the low dimension data (wihtout rest)
plt.figure(figsize=[9,9])
targetColors=['red','gold','seagreen','blue','fuchsia',
              'orange','lime','cyan','salmon','navy']
for i in range(len(targetNames)):
    if targetNames[i] != 'rest':
        plt.plot(PC[targetData.labelInd==i,0],
                 PC[targetData.labelInd==i,1],
                 marker='^', ls='none', c=targetColors[i],
                 label=targetNames[i])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()


# plotting the low dimension data (bottle, scissors and face only)
plt.figure(figsize=[9,9])
targetColors=['red','gold','seagreen','blue','fuchsia',
              'orange','lime','cyan','salmon','navy']
for i in range(len(targetNames)):
    if targetNames[i] in ['bottle', 'scissors', 'face']:
        plt.plot(PC[targetData.labelInd==i,0],
                 PC[targetData.labelInd==i,1],
                 marker='^', ls='none', c=targetColors[i],
                 label=targetNames[i])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()
