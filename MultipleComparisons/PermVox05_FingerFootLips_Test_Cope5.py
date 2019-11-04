import os
import numpy as np
import nibabel as nib
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform

##### PARAMETERS #####
# contrast of interest (from the first level)
contInd = '5'
# the session of interest
indSes = 'test'
# number of permutations
nPerm = 1000

##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Statistics directory from the 2nd level analysis
wfDir = os.path.join(dataDir,'WorkflowOutput')
statDir = os.path.join(wfDir,'FingerFootLips_Test_Cope5/stats_dir/stats/')
# Randomise results directory
permDir = os.path.join(statDir,'Randomise')

# create the FDR directory if it doesnt already exist
if not os.path.exists(permDir):
        os.makedirs(permDir)


##### MERGING COPE IMAGES FROM THE FIRST-LEVEL ANALYSIS
# directory where preprocessed fMRI data is located
baseDir = os.path.join(dataDir, 'BatchOutput_FingerFootLips/feat_dir')
# a list of subjects
subject_list = ['%02d' % i for i in range(1,11)]

# a list of cope images with full path
listCopeFiles = []
for iSubj in subject_list:
    # full path to a cope image
    pathCope = os.path.join(baseDir,
                            'sub-' + iSubj,
                            'ses-' + indSes,
                            'run0.feat',
                            'stats',
                            'cope' + contInd + '.nii.gz')
    listCopeFiles.append(pathCope)

# merged 4D cope image
cope4DImg = os.path.join(permDir,'cope' + contInd + '_4D.nii.gz')

# FSL shell command to merge all cope images
com_merge = 'fslmerge -t ' + cope4DImg
for iCope in listCopeFiles:
    com_merge += ' ' + iCope
res = os.system(com_merge)


##### PERMUTATION TEST WITH RANDOMISE #####
# actual permutation test with Randomise
maskImg = os.path.join(statDir,'mask.nii.gz')
outBase = os.path.join(permDir,'Perm')  # directory and prefix for the output
com_perm = 'randomise -i ' + cope4DImg
com_perm += ' -o ' + outBase
com_perm += ' -m ' + maskImg
com_perm += ' -1 -n ' + str(nPerm) + ' -x'
res = os.system(com_perm)

# thresholding the resulting t-stat image
FWEth = 8.95506  # threshold discovered by permutation
tImg = os.path.join(permDir,'Perm_tstat1.nii.gz')
tFWEthImg = os.path.join(permDir,'Perm_thresh_vox_corrp05_tstat1.nii.gz')
com_thr = 'fslmaths ' + tImg
com_thr += ' -thr ' + str(FWEth)
com_thr += ' ' + tFWEthImg
res = os.system(com_thr)


##### OVERLAY OF SIGNIFICANT BLOBS #####
# T1 weighted image for background
anatDir = os.path.join(dataDir,'derivatives_selected/fmriprep/sub-09/anat/')
imageT1 = os.path.join(anatDir,
                       'sub-09_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')

# Thresholded tstat image
thImageStat=nib.load(tFWEthImg)

# global maximum cooridnates
X_zstat = thImageStat.get_data()  # loading the thresholded zstat image
globalMax = np.unravel_index(np.argmax(X_zstat), X_zstat.shape) # voxel space
globalMaxMNI = coord_transform(globalMax[0],
                               globalMax[1],
                               globalMax[2],
                               thImageStat.affine)  # MNI space

# blob overlay at global max
plot_stat_map(thImageStat, bg_img=imageT1,
              colorbar=True, black_bg=True,
              draw_cross=True,
              cut_coords=globalMaxMNI)

# interactive visualization
view_img(thImageStat, bg_img=imageT1, cmap='black_red',
         symmetric_cmap=False, annotate=True,
         colorbar=True, black_bg=True,
         cut_coords=globalMaxMNI)
