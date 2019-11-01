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
statDir = os.path.join(wfDir,'FingerFootLips_Test_Cope5/stats_dir/stats/')
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
nCope = 10
# Number of regressors in the design matrix
nReg = 1
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


# thresholding the FDR p-image
com_thFDR = 'fslmaths '
com_thFDR += fdrPImg + ' -uthr ' + str(q) + ' ' + fdrThreshImg
res = os.system(com_thFDR)

# masking the z-stat image for significant voxels only for FDR<q
com_thZ = 'fslmaths '
com_thZ += zstatImg + ' -mas ' + fdrThreshImg + ' ' + fdrThreshZImg
res = os.system(com_thZ)



##### OVERLAY OF SIGNIFICANT BLOBS #####
# T1 weighted image for background
anatDir = os.path.join(dataDir,'derivatives_selected/fmriprep/sub-09/anat/')
imageT1 = os.path.join(anatDir,
                       'sub-09_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz')

# Thresholded zstat image
thImageStat=nib.load(fdrThreshZImg)

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
