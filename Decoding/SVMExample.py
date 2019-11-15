import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report


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
targetNames = ['bottle', 'face', 'scissors']  # the ttims of interest
stimMask = targetData.labels.isin(targetNames)  # indices for the stim of interest
X = X_fMRI[stimMask]   # features (for selected stimuli only)
y = np.array(targetData.labelInd)[stimMask]  # labels



##### SVM CLASSIFICATION  (LINEAR WITH C=1)
# spliting the data into training and testing data sets
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.25,
                                                    random_state=0)

# SVM model fitting
sv = SVC(kernel='linear', C=1.0)
sv.fit(X_train,y_train)

# SVM classifier
y_pred = sv.predict(X_test)   # predicted class

# Confusion matrix
print(confusion_matrix(y_test,y_pred))

# classification report
print(classification_report(y_test, y_pred, target_names=targetNames))



###### SEARCHING THE OPTIMAL PARAMETERS
# parameter space
param = {'C': [10,1,0.1,0.01],
         'kernel': ['rbf','poly','linear']}
# classifier object (sans parameters)
svm_grid = SVC()
# grid search object
grid = GridSearchCV(svm_grid, param, cv=5)
grid.fit(X,y)
# best combination
print(grid.best_params_)
# best score
print(grid.best_score_)
