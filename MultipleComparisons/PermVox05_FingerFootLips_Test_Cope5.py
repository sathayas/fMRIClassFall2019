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
maskImg = os.path.join(statDir,'mask.nii.gz')
com_perm = 'randomise -i ' + cope4DImg + '-o Perm '
com_perm += '-m ' + maskImg
com_perm += '-1 -n ' + str(nPerm) + ' -x'
res = os.system(com_perm)