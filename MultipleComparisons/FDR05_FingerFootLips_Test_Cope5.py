import os

##### PARAMETERS #####
# contrast of interest
contInd = '1'

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

# image for the contrast of interest
copeImg = os.path.join(statDir,'cope' + contInd + '.nii.gz')
varcopeImg = os.path.join(statDir,'varcope' + contInd + '.nii.gz')
maskImg = os.path.join(statDir,'mask.nii.gz')

# output image names
logPImg = os.path.join(fdrDir,'logp' + contInd + '.nii.gz') # logP image
PImg = os.path.join(fdrDir,'p' + contInd + '.nii.gz') # P image


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
