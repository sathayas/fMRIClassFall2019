import os
from bids.grabbids import BIDSLayout


# Directory where your data set resides.
dataDir = '/tmp/Data/ds114'

# Creating the layout object for this BIDS data set
layout = BIDSLayout(dataDir)

# subjects
subjList = layout.get_subjects()

# sessions
sesList = layout.get_sessions()

# modalities
modList = layout.get_modalities()

# tasks
taskList = layout.get_tasks()

# runs
runList = layout.get_runs()



# List of all fMRI data for subject 01
fMRI_sub01 = layout.get(subject='01',
                        type='bold',
                        extensions=['nii', 'nii.gz'],
                        return_type='file')

# Lets focus on test session
fMRI_sub01_test = layout.get(subject='01',
                             session='test',
                             type='bold',
                             extensions=['nii', 'nii.gz'],
                             return_type='file')



# A list of files associated with the covert verb generation
# (covertverbgeneration) task
list_covertverbgen = layout.get(task='covertverbgeneration',
                                extensions=['tsv','json'],
                                return_type='file')


# a list of T1w images from everybody
listT1w = layout.get(type='T1w',
                     extensions=['nii','nii.gz'],
                     return_type='file')
