import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nilearn import datasets
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from nilearn.plotting import plot_stat_map

##### PARAMETERS
TR = 2.5

##### DIRECTORY BUSINESS ######
# original data directory where the data resides
dataDir = '/tmp/Data/ds114'
mvpaDataDir = os.path.join(dataDir, 'Data_MotorMVPA')


##### DATA FILES
imgfMRITrain = os.path.join(mvpaDataDir,'bold_train.nii.gz')   # fMRI, training
imgfMRITest = os.path.join(mvpaDataDir,'bold_test.nii.gz')   # fMRI, training
anatDir = os.path.join(dataDir,'derivatives_selected/fmriprep/sub-09/anat/')
imgAnat = os.path.join(anatDir,
                         'sub-09_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')
imgMaskPCG = os.path.join(mvpaDataDir,'aal_MNI_rbPrePoCG.nii.gz')   # pre, post cent gyrus mask
tableTargetTrain = os.path.join(mvpaDataDir,'TaskInfo_Train.csv')  # labels, training
tableTargetTest = os.path.join(mvpaDataDir,'TaskInfo_Test.csv')  # labels, testing



###### EXTRACTING DATA FROM ROI MASK

# Masking the image data with the PCG mask, extracting voxels
masker = NiftiMasker(mask_img=imgMaskPCG,
                     standardize=True,
                     detrend=True,
                     high_pass=0.008, t_r=TR)
# Extracting the voxel time series within the mask
X_fMRI_train = masker.fit_transform(imgfMRITrain)
X_fMRI_test = masker.fit_transform(imgfMRITest)



##### BEHAVIORAL DATA
# loading the behavior data into a dataframe
targetDataTrain = pd.read_csv(tableTargetTrain)
targetDataTest = pd.read_csv(tableTargetTest)
# stimulus types
targetNames = [targetDataTrain[targetDataTrain.NumLabel==x].Label.unique()[0]
                for x in range(6)]


##### SELECTED STIMULI ONLY
stimMaskTrain = targetDataTrain.Label!='Rest'  # indices for stims other than Rest
stimMaskTest = targetDataTest.Label!='Rest'  # indices for stims other than Rest
X_train = X_fMRI_train[stimMaskTrain]   # features (for selected stimuli only)
X_test = X_fMRI_test[stimMaskTest]   # features (for selected stimuli only)
y_train = np.array(targetDataTrain.NumLabel)[stimMaskTrain]  # labels
y_test = np.array(targetDataTest.NumLabel)[stimMaskTest]  # labels



##### SVM CLASSIFICATION  (LINEAR WITH C=1)

# SVM model fitting
sv = SVC(kernel='linear', C=1.0)
sv.fit(X_train,y_train)

# SVM classifier
y_pred = sv.predict(X_test)   # predicted class

# Confusion matrix
print(confusion_matrix(y_test,y_pred))

# classification report
print(classification_report(y_test, y_pred, target_names=targetNames[1:]))





####### VISUALIZING WEIGHTS
coef = sv.coef_   # coefficients for classifier weights
w = ((coef**2).sum(axis=0))**0.5  # squared sum across comparisons

# inverse transformation of weights to the original voxel space
w_img = masker.inverse_transform(w)

# visualizing the weight image
plot_stat_map(w_img, bg_img=imgAnat, title="SVM weights")
