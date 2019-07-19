import os
from bids.layout import BIDSLayout

# Directory where your data set resides.
dataDir = '/tmp/Data/ds114'

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# new subjects
newSubj = list(range(10,19))

# other information for the directory organization
listSes = ['test', 'retest']
listMod = ['anat', 'func', 'dwi']




# first, a list of new subject directories
pattern = "sub-{subject}"
for iSubj in newSubj:
    # dictionary listing entitied
    entities = {'subject':'%02d' % iSubj}
    newDir = layout.build_path(entities, path_patterns=[pattern])
    print(newDir)


# session directories for each subject
pattern = "sub-{subject}/ses-{session}"
for iSubj in newSubj:
    for iSes in listSes:
        # dictionary listing entitied
        entities = {'subject':'%02d' % iSubj,
                    'session':iSes}
        newDir = layout.build_path(entities, path_patterns=[pattern])
        print(newDir)


# image modality directories for each subject
pattern = "sub-{subject}/ses-{session}/{modality}"
for iSubj in newSubj:
    for iSes in listSes:
        for iMod in listMod:
            # dictionary listing entitied
            entities = {'subject':'%02d' % iSubj,
                        'session':iSes,
                        'modality':iMod}
            newDir = layout.build_path(entities, path_patterns=[pattern])
            print(newDir)



# bold fMRI data with different tasks
listTask = ['covertverbgeneration',
            'fingerfootlips',
            'linebisection',
            'overtverbgeneration',
            'overtwordrepetition']
pattern = "sub-{subject}/ses-{session}/{modality}/sub-{subject}_ses-{session}_task-{task}_{type}.nii.gz"
for iTask in listTask:
    entities = {'subject':'01',
                'session':'test',
                'modality':'func',
                'task':iTask,
                'type':'bold'}
    newFile = layout.build_path(entities, path_patterns=[pattern])
    print(newFile)
