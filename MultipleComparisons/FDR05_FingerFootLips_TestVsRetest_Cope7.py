import os
import numpy as np
import nibabel as nib
from nilearn.plotting import plot_stat_map, view_img
from nilearn.image import math_img, coord_transform

##### PARAMETERS #####
# contrast of interest
contInd = '1'
# desired FDR level
q = 0.05

##### DIRECTORY BUSINESS ######
# original data directory
dataDir = '/tmp/Data/ds114'
# Statistics directory from the 2nd level analysis
wfDir = os.path.join(dataDir,'WorkflowOutput')
statDir = os.path.join(wfDir,'FingerFootLips_TestVsRetest_Cope7/stats_dir/stats/')
# FDR results directory
fdrDir = os.path.join(statDir,'FDR')

# create the FDR directory if it doesnt already exist
if not os.path.exists(fdrDir):
        os.makedirs(fdrDir)

# images for the contrast of interest
copeImg = os.path.join(statDir,'cope' + contInd + '.nii.gz')
varcopeImg = os.path.join(statDir,'varcope' + contInd + '.nii.gz')
maskImg = os.path.join(statDir,'mask.nii.gz')
zstatImg = os.path.join(statDir,'zstat' + contInd + '.nii.gz')

# output image names
logPImg = os.path.join(fdrDir,'logp' + contInd + '.nii.gz') # logP image
PImg = os.path.join(fdrDir,'p' + contInd + '.nii.gz') # P image
fdrPImg = os.path.join(fdrDir,'FDRp' + contInd + '.nii.gz') # FDR-corrected P image
fdrThreshImg = os.path.join(fdrDir,'FDRthresh_p' + contInd + '.nii.gz') # thresholded FDR P image
# z-stat image thresholded so that only significant voxels (by FDR) are included
fdrThreshZImg = os.path.join(fdrDir,'FDRthresh_zstat' + contInd + '.nii.gz')


##### T-STATISTIC IMAGE TO P-VALUE IMAGE #####

# calculating error dof
# Number of cope images in the merged cope
nCope = 20
# Number of regressors in the design matrix
nReg = 11
# Degrees of freedom
dof = nCope - nReg

# FSL shell command to convert t-stat image to log p-value image
com_logP = 'ttologp -logpout '
com_logP += logPImg + ' ' + varcopeImg + ' ' + copeImg + ' '
com_logP += str(dof)
res = os.system(com_logP)

# FSL shell command to convert log p-value image to p-value image
com_P = 'fslmaths '
com_P += logPImg + ' -exp ' + PImg
res = os.system(com_P)



##### ACTUAL FDR CORRECTION -- FINDING THE THRESHOLD AND APPLYING #####
# finding the FDR threshold
com_FDR = 'fdr -i '
com_FDR += PImg + ' -m ' + maskImg
com_FDR += ' -q ' + str(q) + ' -a ' + fdrPImg
res = os.system(com_FDR)
