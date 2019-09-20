import os
from shutil import copyfile

# function to create a directory if doesnt exist already
def mkdirIfNotExist(dirPath):
    if os.path.isdir(dirPath) == False:
        os.mkdir(dirPath)


# The ending of filenames of files to be copied
tailfMRI = '_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'
tailfMRIMask = '_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'
tailT1w = '_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz'
tailT1wMask = '_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# directory where fmriprep results reside
resDir = os.path.join(dataDir,'derivatives/fmriprep')

# output directory (create them if they don't exitst)
parentOutDir = os.path.join(dataDir,'derivatives_selected')
mkdirIfNotExist(parentOutDir)
outDir = os.path.join(parentOutDir,'fmriprep')
mkdirIfNotExist(outDir)

# getting a list of subject directories
listDirContents = os.listdir(resDir)
listSubDir = [x for x in listDirContents
              if ('sub-' in x) and ('.html' not in x)]
listSubDir.sort()  # just so that the directories are sorted


# Loop over subjects
for iSubj in listSubjDir:
    # Subject directory in the original data set
    subDir = os.path.join(resDir, iSubj)

    # making a list of T1w files to be copied
    anatDir = os.path.join(subDir,'anat')
    listAnatContents = os.listdir(anatDir)
    filesT1w = [x for x in listAnatContents if tailT1w in x]
    filesT1wMask = [x for x in listAnatContents if tailT1wMask in x]

    # making a list of sessions
    listSesContents = os.listdir(subDir)
    listSes = [x for x in listSesContents if 'ses-' in x]
    if len(listSes)==0:   # if no multiple sessions
        listSes += ['']   # an empty string is added

    # create the subject directory
    subOutDir = os.path.join(outDir,iSubj)
    mkdirIfNotExist(subOutDir)

    # create the anat directory
    anatOutDir = os.path.join(subOutDir,'anat')
    mkdirIfNotExist(anatOutDir)

    # copying T1w and T1w mask images
    for iFile in filesT1w:
        fSource = os.path.join(anatDir, iFile)
        fTarget = os.path.join(anatOutDir, iFile)
        copyfile(fSource, fTarget)
    for iFile in filesT1wMask:
        fSource = os.path.join(anatDir, iFile)
        fTarget = os.path.join(anatOutDir, iFile)
        copyfile(fSource, fTarget)

    # Loop over session directories
    for iSes in listSes:
        # session directory in the original data
        sesDir = os.path.join(subDir,iSes)
        funcDir = os.path.join(sesDir,'func')

        # making a list of fMRI files to be copied
        listFuncContents = os.listdir(funcDir)
        filesfMRI = [x for x in listFuncContents if tailfMRI in x]
        filesfMRIMask = [x for x in listFuncContents if tailfMRIMask in x]

        # create session directories
        sesOutDir = os.path.join(subOutDir,iSes)
        mkdirIfNotExist(sesOutDir)
        funcOutDir = os.path.join(sesOutDir,'func')
        mkdirIfNotExist(funcOutDir)

        # copying fMRI and fMRI mask images
        for iFile in filesfMRI:
            fSource = os.path.join(funcDir, iFile)
            fTarget = os.path.join(funcOutDir, iFile)
            copyfile(fSource, fTarget)
        for iFile in filesfMRIMask:
            fSource = os.path.join(funcDir, iFile)
            fTarget = os.path.join(funcOutDir, iFile)
            copyfile(fSource, fTarget)
