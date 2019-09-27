import os
import pandas as pd
from bids.layout import BIDSLayout

# Directory where your data set resides.
dataDir = '/tmp/Data/ds114'

# Creating the layout objects
layout = BIDSLayout(dataDir)


# Task events tsv file for fingerfootlips, all subjects, both sessions
taskTSV = layout.get(task='fingerfootlips',
                     suffix='events',
                     extension='tsv',
                     return_type='file')[0]

# reading the task info (as pandas data frame)
taskInfo = pd.read_csv(taskTSV, delimiter='\t')

# see whats in the task info
print(taskInfo)
