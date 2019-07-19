import os
import pandas as pd
import matplotlib.pyplot as plt
from bids.layout import BIDSLayout

# Directory where your data set resides.
dataDir = '/tmp/Data/ds102'

# Creating the layout objects
layout = BIDSLayout(dataDir)


# PARTICIPANT INFORMATION

# reading in participant info (tsv read as pandas data frame)
file_participants = layout.get(suffix='participants',
                               extension='tsv',
                               return_type='file')[0]
subjInfo = pd.read_csv(file_participants, delimiter='\t')




# IMAGE META DATA

# Images for sub-01
listImages_sub01 = layout.get(subject='01',
                              extension=['nii', 'nii.gz'],
                              return_type='file')


# meta data asccoiated with T1 weighted
metaT1w = layout.get_metadata(listImages_sub01[0])

# meta data associated with fMRI (run1)
metafMRI = layout.get_metadata(listImages_sub01[1])


# locations of meta data files (T1w)
metalocT1w = layout.get(suffix='T1w',
                        extension='json',
                        return_type='file')



# TASK EVENTS

# Task events tsv file for sub-01, run-1
taskTSV = layout.get(subject='01',
                     run='1',
                     suffix='events',
                     extension='tsv',
                     return_type='file')[0]

# reading the task info (as pandas data frame)
taskInfo = pd.read_csv(taskTSV, delimiter='\t')


# Just for fun. Plotting the response time over experiment
plt.plot(taskInfo[taskInfo.Stimulus=='incongruent'].onset,
         taskInfo[taskInfo.Stimulus=='incongruent'].response_time,
         'r.',
         label='incongruent')
plt.plot(taskInfo[taskInfo.Stimulus=='congruent'].onset,
         taskInfo[taskInfo.Stimulus=='congruent'].response_time,
         'b.',
         label='congruent')
plt.xlabel('Onset')
plt.ylabel('Response time')
plt.legend()
plt.show()
