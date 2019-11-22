import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.plotting import plot_roi, plot_img
from nilearn.input_data import NiftiMasker
from nilearn.image import new_img_like, load_img, index_img, mean_img
from nilearn.decoding import SearchLight
from sklearn.model_selection import KFold



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
tableTarget = haxby_dataset.session_target[0]  # session target table file




###### AREA TO FOCUS ON
voxXmin = 6
voxXmax = 20
voxYmin = 16
voxYmax = 26
voxZmin = 27
voxZmax = 32

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
y = np.array(targetData.labelInd)[stimMask]  # labels
X = index_img(imgfMRI, stimMask)   # selecting only the selected time points
                                         # from the fMRI time series, creating a
                                         # new image object



###### SEARCHLIGHT WITH SVM
cv = KFold(n_splits=5)   # cross-validation splitting object

# The radius is the one of the Searchlight sphere that will scan the volume
searchlight = SearchLight(imgMask,  # mask image object
                          process_mask_img=imgBox,  # voxel block image object
                          radius=5.6,  # radius is 5.6
                          cv=cv)
searchlight.fit(X, y)



###### VISUALIZING THE SEARCHLIGHT RESULTS
# mean fMRI image (i.e., fMRI image without time dimension)
mean_fmri = mean_img(imgfMRI)
# searchlight score image object
searchlight_img = new_img_like(mean_fmri, searchlight.scores_)

# Because scores are not a zero-center test statistics, we cannot use
# plot_stat_map
plot_img(searchlight_img, bg_img=imgAnat,
         title="Searchlight", colorbar=True,
         vmin=.42, cmap='hot', threshold=.5, black_bg=True)
