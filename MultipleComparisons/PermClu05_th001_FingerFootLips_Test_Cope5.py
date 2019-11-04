import os
import scipy
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
# uncorrected p threshold to define clusters
pUnc = 0.001

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
# calculating error dof
# Number of cope images in the merged cope
nCope = 10
# Number of regressors in the design matrix
nReg = 1
# Degrees of freedom
dof = nCope - nReg
# converting p threshold to t threshold
tUnc = scipy.stats.t.ppf(1-pUnc,dof)
# actual permutation test with Randomise
maskImg = os.path.join(statDir,'mask.nii.gz')
outBase = os.path.join(permDir,'PermClus')  # directory and prefix for the output
com_perm = 'randomise -i ' + cope4DImg
com_perm += ' -o ' + outBase
com_perm += ' -m ' + maskImg
com_perm += ' -1 -n ' + str(nPerm) + ' -c ' + str(tUnc)
res = os.system(com_perm)

# thresholding the t-image retaining only the signficant clusters
# t-image to be thresholded
tImg = os.path.join(permDir,'PermClus_tstat1.nii.gz')
# thresholded t-image
tFWEthImg = os.path.join(permDir,'Perm_thresh_clu_corrp05_uncorrp001_tstat1.nii.gz')
# cluster size, FWE corrected
cluFWE = 10
com_clus = 'cluster --in=' + tImg
com_clus += ' --thresh=' + str(tUnc)
com_clus += ' --minextent=' + str(cluFWE)
com_clus += ' --othresh=' + tFWEthImg
res = os.system(com_clus)
