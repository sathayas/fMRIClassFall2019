import os
import numpy as np

# Parameters
TR = 2.5

# data directory business
dataDir = '/tmp/Data/ds114/'
baseDir = os.path.join(dataDir, 'derivatives_selected/fmriprep/')

# merged fMRI data
ffMRI_train = 'bold_train.nii.gz'

# list of subjects to be included
listSub = ['01', '02', '05', '06']
# list of sessions to be included
listSes = ['test', 'retest']
# task of interest
taskName = 'fingerfootlips'

# creating a list of fMRI image data
listfMRI = []
for iSub in listSub:
    for iSes in listSes:
        subjDir = os.path.join(baseDir, 'sub-' + iSub)
        sesDir = os.path.join(subjDir, 'ses-' + iSes)
        funcDir = os.path.join(sesDir, 'func')
        listFiles = os.listdir(funcDir)
        ffMRI = [x for x in listFiles if (taskName in x) and ('_bold.nii.gz' in x)]
        fullffMRI = os.path.join(funcDir, ffMRI[0])
        listfMRI.append(fullffMRI)

# merging fMRI data into a single file
com_merge = 'fslmerge -tr ' + ffMRI_train + ' ' + ' '.join(listfMRI)
com_merge += ' ' + str(TR)
res = os.system(com_merge)



# merged fMRI data
ffMRI_test = 'bold_test.nii.gz'

# list of subjects to be included
listSub = ['09','10']
# list of sessions to be included
listSes = ['test', 'retest']
# task of interest
taskName = 'fingerfootlips'

# creating a list of fMRI image data
listfMRI = []
for iSub in listSub:
    for iSes in listSes:
        subjDir = os.path.join(baseDir, 'sub-' + iSub)
        sesDir = os.path.join(subjDir, 'ses-' + iSes)
        funcDir = os.path.join(sesDir, 'func')
        listFiles = os.listdir(funcDir)
        ffMRI = [x for x in listFiles if (taskName in x) and ('_bold.nii.gz' in x)]
        fullffMRI = os.path.join(funcDir, ffMRI[0])
        listfMRI.append(fullffMRI)

# merging fMRI data into a single file
com_merge = 'fslmerge -tr ' + ffMRI_test + ' ' + ' '.join(listfMRI)
com_merge += ' ' + str(TR)
res = os.system(com_merge)
