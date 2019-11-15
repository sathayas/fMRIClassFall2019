import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.feature_selection import SelectFdr, SelectFwe, f_classif
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from nilearn.plotting import plot_stat_map
from nilearn.image import mean_img
###### PARAMETERS
TR = 2.5


###### LOADING IMAGE DATA
# original data directory where haxby2001 directory resides
dataDir = '/tmp/Data'
# By default 2nd subject will be fetched
haxby_dataset = datasets.fetch_haxby(data_dir=dataDir)
imgfMRI = haxby_dataset.func[0]   # fMRI data file
imgAnat = haxby_dataset.anat[0]   # structural data file
imgMask = haxby_dataset.mask   # brain mask
tableTarget = haxby_dataset.session_target[0]  # session target table file

# Masking the image data with mask, extracting voxels
masker = NiftiMasker(mask_img=imgMask,
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
targetNames = ['bottle', 'face', 'scissors']  # the ttims of interest
stimMask = targetData.labels.isin(targetNames)  # indices for the stim of interest
X_fMRI_selected = X_fMRI[stimMask]   # features (for selected stimuli only)
y = np.array(targetData.labelInd)[stimMask]  # labels




###### FEATURE SELECTION
# FDR feature selector
selector = SelectFdr(f_classif, alpha=0.01)  # FDR selector object
selector.fit(X_fMRI_selected, y)   # learning from the data
X = selector.transform(X_fMRI_selected)   # Selected features only
indVoxels = selector.get_support(indices=True)   # indices of surviving voxels


###### VISUALIZING FEATURE LOCATIONS
# binary vector with 1s indicating selected voxels
bROI = np.zeros(X_fMRI.shape[-1])
bROI[indVoxels] = 1
# reverse masking
bROI_img = masker.inverse_transform(bROI)

# Create the figure
plot_stat_map(bROI_img, imgAnat, title='Voxels surviving FDR')



###### SVM CLASSIFIER
